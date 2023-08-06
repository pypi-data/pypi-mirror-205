from functools import cached_property
import random

from bs4 import BeautifulSoup, Tag, NavigableString

def stripped_text(text):
    return ' '.join(text.split())

def text_to_html(tag, text, new_line_after_tag=False):
    if not text:
        return ''
    
    if new_line_after_tag:
        html_text = f'<{tag}>\n{text}</{tag}>' if tag else text
    else:
        html_text = f'<{tag}>{text}</{tag}>' if tag else text
    html_text = html_text + '\n'
    return html_text

def add_tag_to_contexts(strings, tag=None):
    if not strings or not tag or tag == '[document]':
        return strings

    first_non_empty = None
    last_non_empty = None

    # Find first and last non-empty strings
    for i, s in enumerate(strings):
        if s.strip():
            if first_non_empty is None:
                first_non_empty = i
            last_non_empty = i

    # If no non-empty strings, return the original list
    if first_non_empty is None:
        return strings

    # Prepend <TAG> to the first non-empty string
    strings[first_non_empty] = f'<{tag}>\n{strings[first_non_empty]}'

    # Append </TAG> to the last non-empty string
    strings[last_non_empty] = f'{strings[last_non_empty]}</{tag}>\n'

    return strings


class HTMLObject:
    
    # TAGS = ['p', 'ul', 'ol', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a']
    # TAGS = ['p', 'ul', 'ol', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span']
    TAGS = ['p', 'ul', 'ol', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'span']
    MAX_DEPTH = 100
    
    def __init__(self, html, is_soup=False, depth=0):
        
        soup = BeautifulSoup(html, features='lxml') if not is_soup else html

        self.depth = depth
        self.soup = soup
        self.tag = soup.name if soup.name else ''
        self.text = stripped_text(soup.text)
        self.included_in_excerpt = False
        self.is_context_before = False
        self.is_context_after = False
        
    @classmethod
    def _search_tags(cls, soup, tags=TAGS):
    
        elements = []
        if soup.text.strip() and isinstance(soup, Tag):
            for child in soup.children:
                if (child.name in tags or isinstance(child, NavigableString)) and child.text.strip():
                    elements.append(child)
                else:
                    elements.extend(cls._search_tags(child, tags))
                
        return elements
        
    @cached_property
    def elements(self):

        if self.depth > self.MAX_DEPTH:
            return []
        
        elements = []
        
        if self.tag in ['ul', 'ol']:
            list_items = self.soup.find_all('li', recursive=False)
            elements = [HTMLObject(item, is_soup=True, depth=self.depth + 1) for item in list_items if item.text]
        else:
            element_tags = self._search_tags(self.soup)
            elements = [HTMLObject(tag, is_soup=True, depth=self.depth + 1) for tag in element_tags if tag.text]
            
        return elements
    
    @cached_property
    def elements_recursive(self):
        elements = []
        for e in self.elements:
            if e.is_terminal:
                elements.append(e)
            else:
                elements.extend(e.elements_recursive)
        return elements
    
    @cached_property
    def is_terminal(self):
        return len(self.elements) == 0
    
    def _collect_text(self, excerpt=True):
        
        text = ''
        
        if excerpt and not self.included_in_excerpt and self.is_terminal:
            return text
        
        if self.is_terminal:
            if self.text:
                text = text_to_html(self.tag, self.text)
        else:
            children_text = ''
            for child in self.elements:
                children_text = children_text + child._collect_text(excerpt)
            
            if children_text:
                if excerpt and self.tag == '[document]':
                    text = children_text
                else:
                    text = text_to_html(self.tag, children_text, new_line_after_tag=True)
                
        return text
    
    def _collect_text_with_context(self):
        
        context_before = ''
        context_after = ''
        text = ''

        included = self.included_in_excerpt or self.is_context_before or self.is_context_after
        
        if not included and self.is_terminal:
            return text, context_before, context_after
        
        if self.is_terminal:
            if self.text:
                if self.is_context_before:
                    context_before = text_to_html(self.tag, self.text)
                elif self.is_context_after:
                    context_after = text_to_html(self.tag, self.text)
                else:
                    text = text_to_html(self.tag, self.text)
        else:
            children_text = ''
            children_context_before = ''
            children_context_after = ''
            for child in self.elements:

                child_text, child_context_before, child_context_after = child._collect_text_with_context()
                
                children_text = children_text + child_text
                children_context_before = children_context_before + child_context_before
                children_context_after = children_context_after + child_context_after

            # text, context_before, context_after = contexts_to_html(children_text, children_context_before, children_context_after, self.tag)
            context_before, text, context_after = add_tag_to_contexts([children_context_before, children_text, children_context_after], self.tag)
                
        return text, context_before, context_after

class HTMLDocument(HTMLObject):
    def __init__(self, html):
        super().__init__(html, is_soup=False, depth=0)
        
    def reset(self):
        # Undo previous excerpt
        for e in self.elements_recursive:
            e.included_in_excerpt = False
            e.is_context_before = False
            e.is_context_after = False
        
    def random_excerpt(self, n_items=5, include_context=False, n_context_items=2, seed=None):

        if seed:
            random.seed(seed)

        self.reset()
        max_start = max(len(self.elements_recursive) - n_items, 0)
        
        start = random.randint(0, max_start)
        end = start + n_items
        
        for e in self.elements_recursive[start:end]:
            e.included_in_excerpt = True

        if include_context:
            context_start = max(start - n_context_items, 0)
            for e in self.elements_recursive[context_start:start]:
                e.is_context_before = True

            context_end = min(end + n_context_items, len(self.elements_recursive))
            for e in self.elements_recursive[end:context_end]:
                e.is_context_after = True

            return self._collect_text_with_context()

        return self._collect_text()

    @cached_property
    def full_text(self):
        text = self._collect_text(excerpt=False)

        # Replace soft hyphens, see https://stackoverflow.com/questions/51976328/best-way-to-remove-xad-in-python
        text = text.replace('\xad', '') # Soft hyphen
        text = text.replace('\u200b', '') # Zero-width space
        return text

    @classmethod
    def inner_text(cls, text):

        start_index = text.index('<[document]>\n') + len('<[document]>\n')
        end_index = text.index('\n</[document]>')

        return text[start_index:end_index]
