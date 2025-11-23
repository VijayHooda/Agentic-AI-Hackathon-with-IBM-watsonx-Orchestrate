# sample_data.py
# Small mock dataset representing past deals for similarity retrieval.

PAST_DEALS = [
    {
        "deal_id": "D001",
        "company": "Acme Cloud",
        "industry": "SaaS",
        "size": "Mid",
        "summary": "Acme Cloud wanted to reduce infra costs; we offered cost-optimization + managed infra; closed in 6 weeks; ARR $120k",
        "outcome": "Won"
    },
    {
        "deal_id": "D002",
        "company": "RetailCorp",
        "industry": "Retail",
        "size": "Large",
        "summary": "RetailCorp required real-time inventory analytics; PoC failed due to incomplete data; lost.",
        "outcome": "Lost"
    },
    {
        "deal_id": "D003",
        "company": "FinSys",
        "industry": "FinTech",
        "size": "Mid",
        "summary": "FinSys needed compliance automation; pilot deployed and upsell into core; ARR $200k",
        "outcome": "Won"
    },
    {
        "deal_id": "D004",
        "company": "HealthPlus",
        "industry": "Healthcare",
        "size": "Small",
        "summary": "HealthPlus wanted telehealth integration; pilot success; closed after 3 months; ARR $40k",
        "outcome": "Won"
    },
    {
        "deal_id": "D005",
        "company": "LogistiX",
        "industry": "Logistics",
        "size": "Large",
        "summary": "LogistiX sought route optimization; technical fit but procurement delays; still in pipeline.",
        "outcome": "Stalled"
    }
]
