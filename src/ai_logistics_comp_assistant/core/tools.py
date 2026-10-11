import logging
import sqlite3
from pathlib import Path

from pydantic import BaseModel
from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper

logger = logging.Logger(__name__)

DB_PATH = Path(__file__).parent.parent / "data" / "greatglobe.db"

class ShippingDetails(BaseModel):
    source: str
    destination: str
    product_name: str
    category: str
    hs_code: str


def get_product_names() -> list[str]:
    """Return unique product names for the shipment form."""
    query = (
        "SELECT DISTINCT Product_Name FROM products "
        "WHERE Product_Name IS NOT NULL ORDER BY Product_Name COLLATE NOCASE"
    )

    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(query).fetchall()

    return [row[0] for row in rows]


@tool
def get_product_details(product_name: str, limit: int = 100) -> dict:
    """
    Use this tool to query Products DB table to fetch product details.

    Args:
        product_name: Exact product name

    Returns:
        dict: Dict with Product_Name, Category and HS_Code
    """

    query = (
        "SELECT Category, Product_Name, HS_Code FROM products "
        "WHERE Product_Name = ? LIMIT ?"
    )

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(query, (product_name, limit))
        row = cursor.fetchone()

    if row:
        return {"Category": row[0], "Product_Name": row[1], "HS_Code": row[2]}
    else:
        return {"message": "Product details not found"}


@tool
def search_shipping_requirements(shipping_details: ShippingDetails, max_results: int = 5) -> str:
    """
    Use this tool to search for compliance and customs requirements
    for shipping a product from source country to destination country.
    Args:
        shipping_details: ShippingDetails object containing source, destination, product_name, category, and hs_code.
        max_results: Maximum number of search results to return.
    """

    query = (f"international trade regulations including import/export documentation, customs duties, and payment procedures "
                f"to ship {shipping_details.product_name} under category {shipping_details.category} with HS code {shipping_details.hs_code} "
                f"from {shipping_details.source} to {shipping_details.destination}" 
            )

    search = DuckDuckGoSearchResults(
        max_results=max_results,
        api_wrapper=DuckDuckGoSearchAPIWrapper(backend="html"),
    )

    try:
        return search.run(query)
    except Exception as error:
        logger.warning("Shipping requirements search failed: %s", error)
        return (
            "Live web search is unavailable. "
            "Do not infer current country-specific requirements; tell the user "
            "that official customs sources must be checked before shipment."
        )
