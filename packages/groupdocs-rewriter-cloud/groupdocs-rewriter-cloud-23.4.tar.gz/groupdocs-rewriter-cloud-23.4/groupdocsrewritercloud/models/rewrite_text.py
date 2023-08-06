# coding: utf-8
# """Copyright
# --------------------------------------------------------------------------------------------------------------------
# <copyright company="Aspose" file="rewrite_text.py">
# Copyright (c) 2022 GroupDocs.Rewriter Cloud
# </copyright>
# <summary>
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# </summary>
# --------------------------------------------------------------------------------------------------------------------
# """

"""
 * Creates body for text rewriting request
"""
import json


class RewriteText:
    """
        Attributes:
          model_types (dict):   The key is attribute name
                                and the value is attribute type.
          attribute_map (dict): The key is attribute name
                                and the value is json key in definition.
        """
    model_types = {
        'Language': 'str',
        'Text': 'str',
        'Tokenize': bool,
        'Diversity': 'str',
        'Suggestions': int
    }

    attribute_map = {
        'Language': 'language',
        'Text': 'text',
        'Tokenize': 'tokenize',
        'Diversity': 'diversity',
        'Suggestions': 'suggestions'
    }

    def __init__(self, language, text, tokenize=False, diversity="off", suggestions=1):
        """
        :param str language: language of text
        :param str text: text to paraphrase
        :param bool tokenize: to tokenize input and output texts
        :param str diversity: diversity level of output text
        :param int suggestions: number of paraphrasing variants returned
        """
        self.Language = language  # language of text
        self.Text = text  # text to paraphrase
        self.Tokenize = tokenize  # tokenization mode
        self.Diversity = diversity  # diversity of paraphrasing, "medium" or "high", default is "off"
        self.Suggestions = suggestions  # number of suggested variants, 3 maximum

    def to_string(self):
        request = [{"language": self.Language, "text": self.Text, "tokenize": self.Tokenize,
                    "diversity": self.Diversity, "suggestions": self.Suggestions}]
        return json.dumps(request)
