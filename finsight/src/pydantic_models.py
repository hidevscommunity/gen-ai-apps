from pydantic import BaseModel, Field

min_length = 40

class IncomeStatementInsights(BaseModel):
    revenue_health: str = Field(..., description=f"Must be more than {min_length} words. Insight into the company's total revenue, providing a perspective on the health of the primary business activity.")
    operational_efficiency: str = Field(..., description=f"Must be more than {min_length} words. Analysis of the company's operating expenses in relation to its revenue, offering a view into the firm's operational efficiency.")
    r_and_d_focus: str = Field(..., description=f"Must be more than {min_length} words. Insight into the company's commitment to research and development, signifying its emphasis on innovation and future growth.")
    debt_management: str = Field(..., description=f"Must be more than {min_length} words. Analysis of the company's interest expenses, highlighting the scale of its debt obligations and its approach to leveraging.")
    profit_retention: str = Field(..., description=f"Must be more than {min_length} words. Insight into the company's net income, showcasing the amount retained post all expenses, which can be reinvested or distributed.")

class BalanceSheetInsights(BaseModel):
    liquidity_position: str = Field(..., description=f"Must be more than {min_length} words. Insight into the company's ability to meet its short-term obligations using its short-term assets.")
    operational_efficiency: str = Field(..., description=f"Must be more than {min_length} words. Analysis of how efficiently the company is using its assets to generate sales.")
    capital_structure: str = Field(..., description=f"Must be more than {min_length} words. Insight into the company's financial leverage and its reliance on external liabilities versus internal equity.")
    inventory_management: str = Field(..., description=f"Must be more than {min_length} words. Analysis of the company's efficiency in managing, selling, and replacing its inventory.")
    overall_solvency: str = Field(..., description=f"Must be more than {min_length} words. Insight into the company's overall ability to meet its long-term debts and obligations.")

class CashFlowInsights(BaseModel):
    operational_cash_efficiency: str = Field(..., description=f"Must be more than {min_length} words. Insight into how efficiently the company is generating cash from its core operations.")
    investment_capability: str = Field(..., description=f"Must be more than {min_length} words. Indicates the company's ability to invest in its business using its operational cash flows.")
    financial_flexibility: str = Field(..., description=f"Must be more than {min_length} words. Demonstrates the cash left after all operational expenses and investments, which can be used for dividends, share buybacks, or further investments.")
    dividend_sustainability: str = Field(..., description=f"Must be more than {min_length} words. Indicates the company's ability to cover its dividend payouts with its net earnings.")
    debt_service_capability: str = Field(..., description=f"Must be more than {min_length} words. Analysis of the company's ability to service its debt using the operational cash flows.")


class FiscalYearHighlights(BaseModel):
    performance_highlights: str = Field(..., description="Key performance metrics and financial stats over the fiscal year.")
    major_events: str = Field(..., description="Highlight of significant events, acquisitions, or strategic shifts that occurred during the year.")
    challenges_encountered: str = Field(..., description="Challenges the company faced during the year and, if and how they managed or overcame them.")
    milestone_achievements: str = Field(..., description="Milestones achieved in terms of projects, expansions, or any other notable accomplishments.")


class StrategyOutlookFutureDirection(BaseModel):
    strategic_initiatives: str = Field(..., description="The company's primary objectives and growth strategies for the upcoming years.")
    market_outlook: str = Field(..., description="Insights into the broader market, competitive landscape, and industry trends the company anticipates.")
    product_roadmap: str = Field(..., description="Upcoming launches, expansions, or innovations the company plans to roll out.")

class RiskManagement(BaseModel):
    risk_factors: str = Field(..., description="Primary risks the company acknowledges.")
    risk_mitigation: str = Field(..., description="Strategies for managing these risks.")

class CorporateGovernanceSocialResponsibility(BaseModel):
    board_governance: str = Field(..., description="Details about the company's board composition, governance policies, and any changes in leadership or structure.")
    csr_sustainability: str = Field(..., description="The company's initiatives related to environmental stewardship, community involvement, and ethical practices.")

class InnovationRnD(BaseModel):
    r_and_d_activities: str = Field(..., description="Overview of the company's focus on research and development, major achievements, or breakthroughs.")
    innovation_focus: str = Field(..., description="Mention of new technologies, patents, or areas of research the company is diving into.")
