import re
import util

class HtmlInstructionsParser(object):

    TOWARD = 'TOWARD'
    TOWARDS = 'TOWARDS'
    TURN = 'TURN'
    ONTO = 'ONTO'
    ON = 'ON'
    HEAD = 'HEAD'
    DESTINATION = 'DESTINATION'

    KEYWORDS = [TOWARD, TURN, ONTO, ON, HEAD]

    def __init__(self, html_instructions):
        self.html_instructions = html_instructions
        self.instructions = util.strip_html(self.html_instructions)
        self.tokens = self.tokenize()
        self.turn_street = self.get_turn_street()
        self.toward_street = self.get_toward_street()
        self.turn_direction = self.get_turn_direction()
        self.destination_direction = self.get_destination_direction()
        self.on_street = self.get_on_street()

    def tokenize(self):

        tokens = []

        tokens_chars = []
        ignore = False
        tag_open = False
        turn_off_ignore = False
        for s in self.html_instructions:
            if s == '<':
                ignore = True
            elif s == '>':
                turn_off_ignore = True
                if not tag_open:
                    tag_open = True
                else:
                    tag_open = False
            if not ignore:
                if s == ' ' and tokens_chars and not tag_open:
                    tokens.append(''.join(tokens_chars))
                    tokens_chars = []
                else:
                    tokens_chars.append(s)
            if turn_off_ignore:
                ignore = False
                turn_off_ignore = False
        if tokens_chars and not tag_open:
            tokens.append(''.join(tokens_chars))

        processed_tokens = []
        for token in tokens:
            added = False
            for keyword in self.KEYWORDS:
                if token.upper() == keyword.upper():
                    processed_tokens.append(keyword)
                    added = True
                    break
            if not added:
                processed_tokens.append(token)

        return processed_tokens

    def get_toward_street(self):
        return self._get_token_after_word(self.TOWARD) or self._get_token_after_word(self.TOWARDS)

    def get_on_street(self):
        return self._get_token_after_word(self.ON) or self._get_token_after_word(self.ONTO)

    def get_destination_direction(self):
        return self._get_token_after_word(self.DESTINATION, 5)

    def get_turn_direction(self):
        return self._get_token_after_word(self.TURN)

    def get_turn_street(self):
        return self._get_token_after_word(self.TURN, 3)

    def _get_token_after_word(self, word, places=1):
        try:
            word_idx = self.tokens.index(word)
            return self.tokens[word_idx + places]
        except:
            print 'FAIL:', word, places
            return None
