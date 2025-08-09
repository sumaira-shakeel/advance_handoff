

from agents import Agent, Runner, handoff
import asyncio
from connection import config

billing_agent = Agent(
    name="Billing Agent",
    instructions="You just give the answer which are related to billing."
)

refund_agent = Agent(
    name="Refund Agent",
    instructions="You just give the answer which are related to Refund."
)

costum_refund_handoff = handoff(
    agent=refund_agent,  # Fixed here
    tool_name_override="custom_refund_tool",
    tool_description_override="Handle user refund request with extra care."
)
damage_refund_handoff = handoff(
    agent=refund_agent,  # Fixed here
    tool_name_override="damage_refund_tool",
    tool_description_override="Handle refund due to damaged items."
)
late_delivery_refund_handoff = handoff(
    agent=refund_agent,  # Fixed here
    tool_name_override="late_delivery_refund_tool",
    tool_description_override="Handle refund due to late delivery."
)

triage_agent = Agent(
    name="Triage Agent",
    instructions="First read the user request, then decide which agent is best for this work, and give this work to the appropriate agent.",
    handoffs=[billing_agent, costum_refund_handoff,damage_refund_handoff,late_delivery_refund_handoff]
)

async def main():
    user_input = "My product arrived 10 days late. I want the refund.."
    result = await Runner.run(triage_agent, user_input, run_config=config)
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
