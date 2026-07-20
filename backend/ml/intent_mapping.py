from enum import Enum


class AgentType(str, Enum):

    ORDER = "order"

    REFUND = "refund"

    TECHNICAL_SUPPORT = "technical_support"

    GENERAL = "general"


INTENT_TO_AGENT = {

    # Order / Delivery related intents
    11: AgentType.ORDER,
    12: AgentType.ORDER,

    # Refund / Payment related intents
    51: AgentType.REFUND,
    52: AgentType.REFUND,
    53: AgentType.REFUND,

    # Technical Support related intents
    0: AgentType.TECHNICAL_SUPPORT,
    14: AgentType.TECHNICAL_SUPPORT,
    23: AgentType.TECHNICAL_SUPPORT,
    25: AgentType.TECHNICAL_SUPPORT,
    27: AgentType.TECHNICAL_SUPPORT,
    35: AgentType.TECHNICAL_SUPPORT,
    44: AgentType.TECHNICAL_SUPPORT,
    49: AgentType.TECHNICAL_SUPPORT,
    59: AgentType.TECHNICAL_SUPPORT,
    61: AgentType.TECHNICAL_SUPPORT,
    72: AgentType.TECHNICAL_SUPPORT,
}


def get_agent_for_intent(
    intent: int
) -> AgentType:

    return INTENT_TO_AGENT.get(
        intent,
        AgentType.GENERAL
    )