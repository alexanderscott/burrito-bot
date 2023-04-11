from unittest import TestCase

from chalicelib.slack_reaction import SlackReaction
from tests.fixtures.reactions import *


class SlackReactionTestCase(TestCase):

    def test_parse_reaction_emoji_add(self):
        rxn = SlackReaction.parse(reaction_added_emoji())

        self.assertEquals(rxn.recipients, ['U025RUT3QQM'])
        self.assertEquals(rxn.sender, 'U01AP4BM8SD')

