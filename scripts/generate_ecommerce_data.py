from pathlib import Path
import json
import numpy as np
import pandas as pd

#=======================================
#PROJECT CONFIGURATION
#=======================================

BASE_DIR=Path(__file__).resolve().parent
SOURCE_DIR=BASE_DIR/"data"/"source"
INCREMENTAL_DIR=BASE_DIR/"data"/"incremental"
TEST_DIR=BASE_DIR/"data"/"test_data"

#Reproducible data:running the script again produces
#the same base datasets.
rng=np.random.default_rng(42)

CUSTOMER_COUNT=10_000
PRODUCT_COUNT=1_000
ORDER_COUNT=50_000
ORDER_ITEM_COUNT=100_000
PAYMENT_COUNT=50_000
RETURN_COUNT=5_000
EVENT_COUNT=100_000

def create_directories():
    """Create project directories if they don't exist."""

    for directory in [SOURCE_DIR,INCREMENTAL_DIR,TEST_DIR]:
        directory.mkdir(parents=True, exist_ok=True)

def save_csv(df,filename,directory=SOURCE_DIR):
    """save a DataFrame as a CSV file."""

    path=directory/filename

    df.to_csv(path,index=False)

    print(
        f"Created {path.relative_to(BASE_DIR)}"
          F"| Rows: {len(df):,}"
        )
def generate_customers():
        """Generate customer master data."""

        customer_ids=np.arange(
            100001,
            100001+CUSTOMER_COUNT
    )

        first_names=[
            "Rahul","Priya","Amit","Sneha","Arjun",
            "Neha","Vikram","Ananya","kiran","Meera",
            "Rohan","pooja","Sanjay","Divya","Manish"
        ]
        last_names=[
            "Sharma","Reddy","Kumar","Patel","Singh",
            "Rao","Gupta","Verma","Das","Naidu",
            "Khan","Joshi","Iyer","Mishra","Pillai"
        ]

        cities=[
            "Hyderabad","Bengaluru","Chennai","Mumbai",
            "Pune","Delhi","kolkata","Ahmedabad",
            "Jaipur","kochi"
        ]
        states=[
            "Telangana","Karnataka","Tamil Nadu",
            "Maharashtra","Maharashtra","Delhi",
            "West Bengal","Gujarat","Rajasthan","kerala"
        ]
        city_indices=rng.integers(0,len(cities),CUSTOMER_COUNT)
        registration_dates=(
            pd.Timestamp("2023-01-01") + 
            pd.to_timedelta(
                rng.integers(0, 1200, CUSTOMER_COUNT),
                unit='D'
            )
        )
        customers=pd.DataFrame({
            "customer_id":customer_ids,
            "first_name":rng.choice(first_names,CUSTOMER_COUNT),
            "last_name":rng.choice(last_names,CUSTOMER_COUNT),
            "email":[f"customer{customer_id}@example.com"
                     for customer_id in customer_ids],
            "city":[cities[index] for index in city_indices],
            "state":[states[index] for index in city_indices],
            "registration_date":registration_dates,
            "updated_at":registration_dates
        })
        return customers

def generate_products():
        """generate product master data."""

        categories={
            "Men":["T-Shirt","Jeans","Shirt","Jacket"],
            "Women":["Dress","Top","Jeans","skirt"],
            "kids":["T-Shirt","Shorts","Jacket","Dress"],
            "Footwear":["Sneakers","Sandals","Formal Shoes"],
            "Accessories":["Watch","Bag","Belt","Wallet"]
        }
        product_ids=np.arange(200001,200001+ PRODUCT_COUNT)
        category_names=list(categories.keys())
        selected_categories=rng.choice(category_names,PRODUCT_COUNT)
        product_names=[
            f"{category} {rng.choice(categories[category])}"
            f"{index+1}"
            for index,category in enumerate(selected_categories)
        ]
        products=pd.DataFrame({
            "product_id":product_ids,
            "product_name":product_names,
            "category":selected_categories,
            "unit_price":np.round(
                rng.uniform(199,4999,PRODUCT_COUNT),2
            ),
            "stock_quantity":rng.integers(0,1000,PRODUCT_COUNT),
            "is_active":rng.choice([True,False],PRODUCT_COUNT,p=[0.9,0.1]),
            "created_at":(pd.Timestamp("2023-01-01") + 
                pd.to_timedelta(
                    rng.integers(0, 1200, PRODUCT_COUNT),
                    unit='D'
                )
        )
         })
        return products
def generate_orders(customers):
        """Generate order header records."""
        order_ids=np.arange(500001,500001+ORDER_COUNT)
        customer_ids=rng.choice(customers["customer_id"].to_numpy(),ORDER_COUNT)
        start_date=pd.Timestamp("2025-01-01")
        end_date=pd.Timestamp("2026-10-01")
        total_seconds=int(
        (end_date-start_date).total_seconds()
        )
        order_dates=(
            start_date+ pd.to_timedelta(
                rng.integers(0,total_seconds,ORDER_COUNT),
                unit='s'
            )
        )
        order_statuses=[
            "COMPLETED","PENDING","CANCELLED","PROCESSING","SHIPPED"
        ]
        orders=pd.DataFrame({
            "order_id":order_ids,
            "customer_id":customer_ids,
            "order_date":order_dates,
            "order_status":rng.choice(order_statuses,ORDER_COUNT,p=[0.70,0.08,0.07,0.08,0.07],
            ),
            "shipping_city":rng.choice(
                [
                    "Hyderabad","Bengaluru","Chennai",
                    "Mumbai","Pune","Delhi","Kolkata"
                ],
                ORDER_COUNT
            ),
            "updated_at":order_dates
        })
        return orders
def generate_order_items(orders,products):
        """Generate order line items with valid foreign keys."""
        product_ids=products["product_id"].to_numpy()
        product_price_map=products.set_index(
            "product_id"
        )["unit_price"]
        order_ids=orders["order_id"].to_numpy()
        item_order_ids=rng.choice(
        order_ids,
        ORDER_ITEM_COUNT,
        replace=True
        )
        item_product_ids=rng.choice(
            product_ids,
            ORDER_ITEM_COUNT,
            replace=True
        )
        quantities=rng.integers(
            1,6,ORDER_ITEM_COUNT
        )
        unit_prices=product_price_map.loc[
            item_product_ids
        ].to_numpy()

        items=pd.DataFrame({
            "order_item_id":np.arange(90001,90001+ORDER_ITEM_COUNT),
            "order_id":item_order_ids,
            "product_id":item_product_ids,
            "quantity":quantities,
            "unit_price":unit_prices,
            "discount_amount":np.round(
                unit_prices*quantities*rng.uniform(0,0.20,ORDER_ITEM_COUNT),2
            )
        })
        items["line_total"]=np.round(
            items["quantity"]*items["unit_price"]-items["discount_amount"],2
        )
        return items
def generate_payments(orders):
        """Generate one payment record per order."""
        payment_methods=["UPI","CREDIT_CARD","DEBIT_CARD","NET_BANKING","COD"]
        payment_statuses=["SUCCESS","FAILED","PENDING","REFUNDED"]
        payment_ids=np.arange(700001,700001+PAYMENT_COUNT)
        payments=pd.DataFrame({
            "payment_id":payment_ids,
            "order_id":orders["order_id"].to_numpy(),
            "payment_method":rng.choice(
                payment_methods,PAYMENT_COUNT
            ),
            "payment_status":rng.choice(
                payment_statuses,PAYMENT_COUNT,p=[0.82,0.08,0.07,0.03]
            ),
            "payment_date":orders["order_date"].to_numpy(),
            "transaction_reference":[
                f"TXN{payment_id}"
                for payment_id in payment_ids
            ]
        })
        return payments
def generate_returns(order_items):
        """Generate return records referencing valid order items."""
        selected_indices=rng.choice(
            order_items.index.to_numpy(),
            RETURN_COUNT,
            replace=False
        )
        selected_items=order_items.loc[
            selected_indices
        ].reset_index(drop=True)
        return_reasons=[
            "Damaged Product",
            "Wrong Size",
            "Wrong Product",
            "Changed Mind",
            "Product Not as Described"
        ]
        return_dates=(
            pd.Timestamp("2025-01-01") +
            pd.to_timedelta(
                rng.integers(
                    0,
                     int(
                        (
                    pd.Timestamp("2026-10-19") - pd.Timestamp("2025-01-01")
                        ).days
                     ),
                     RETURN_COUNT
                ),
                unit='D'
            )
        )
        returns=pd.DataFrame({
            "return_id":np.arange(800001,800001+RETURN_COUNT),
            "order_item_id":selected_items["order_item_id"].to_numpy(),
            "return_date":return_dates,
            "return_reason":rng.choice(
                return_reasons,RETURN_COUNT
            ),
            "return_status":rng.choice(
                ["APPROVED","PENDING","REJECTED"],RETURN_COUNT,p=[0.75,0.15,0.10]
            )
        })
        return returns
def generate_website_events(customers,products):
        """Generate website event records in JSON Lines format."""
        event_types=["PAGE_VIEW","PRODUCT_VIEW","ADD_TO_CART","CHECKOUT","PURCHASE"]
        customer_ids=customers["customer_id"].to_numpy()
        product_ids=products["product_id"].to_numpy()
        event_times=(
            pd.Timestamp("2026-01-01")+
            pd.to_timedelta(
                rng.integers(
                    0,
                    290*24*60*60,
                    EVENT_COUNT
                ),
                unit='s'
            )
        )
        events=pd.DataFrame({
            "event_id": np.arange(
                1000001,
                1000001 + EVENT_COUNT
            ),
            "customer_id": rng.choice(
                customer_ids,
                EVENT_COUNT
            ),
            "product_id":rng.choice(
                product_ids,
                EVENT_COUNT
            ),
            "event_types":rng.choice(
                event_types,
                EVENT_COUNT
            ),
            "event_timestamp":event_times,
            "device_type":rng.choice(
                ["MOBILE","DESKTOP", "TABLET"],
                EVENT_COUNT,
                p=[0.65, 0.30, 0.05]
            )
        })
        return events   
def create_incremental_data(orders,customers):
        """Create a separate batch containing new and changed records."""
        #Select new orders with fresh IDs.
        new_orders=orders.tail(100).copy()
        new_orders["order_id"]=np.arange(
            900001,900001+len(new_orders)
        )
        new_orders["order_date"]=(
            pd.Timestamp("2026-10-19")
            +pd.to_timedelta(
                np.arange(len(new_orders)),
                unit="m"
            )
        )
        new_orders["updated_at"]=new_orders["order_date"]
        #Select existing customers and simulate changes.
        changed_customers=customers.head(50).copy()
        changed_customers["city"]="Hyderabad"
        changed_customers["updated_at"]=(
            pd.Timestamp("2026-10-19 10:00:00")
        )
        save_csv(
            new_orders,
            "orders_incremental.csv",
            INCREMENTAL_DIR
        )
        save_csv(
            changed_customers,
            "customers_incremental.csv",
            INCREMENTAL_DIR
        )
def create_quality_test_data(orders):
        """Create intentional quality issues for testing."""
        test_orders=orders.head(100).copy()

        #Introduce duplicate order records.
        test_orders=pd.concat(
            [test_orders,test_orders.iloc[[0,1]]],
            ignore_index=True
        )
        #Introduce missing order ID
        test_orders.loc[2, "order_id"] =np.nan

        #Introduce missing customer ID
        test_orders.loc[3,"customer_id"]=np.nan

        #Introduce an invalid date.
        test_orders["order_date"]=test_orders["order_date"].astype("object")

        #Introduce an invalid date.
        test_orders.loc[4,"order_date"]="INVALID_DATE"
        save_csv(
            test_orders,
            "orders_quality_issues.csv",
            TEST_DIR
        )
def main():
        """Generate all project datasets."""
        create_directories()
        print("\n Generating e-commerce source data...\n")
        customers=generate_customers()
        products=generate_products()
        orders=generate_orders(customers)
        order_items=generate_order_items(orders,products)
        payments=generate_payments(orders)
        returns=generate_returns(order_items)
        website_events=generate_website_events(
            customers,products
        )
        save_csv(customers,"customer.csv")
        save_csv(products,"products.csv")
        save_csv(orders,"orders.csv")
        save_csv(order_items,"order_items.csv")
        save_csv(payments,"payments.csv")
        save_csv(returns,"returns.csv")
        events_path=SOURCE_DIR/"website_events.json"
        website_events.to_json(
            events_path,
            orient="records",
            lines=True,
            date_format="iso"
        )
        print(
            f"Created {events_path.relative_to(BASE_DIR)}"
            f"| Rows: {len(website_events):,}"
        ) 

        create_incremental_data(orders,customers)
        create_quality_test_data(orders)

        #Save a data dictionary for the source datasets.
        data_dictionary={
            "customers.csv":{
                "primary_key":"customer_id",
                "description":"Customer master records"
            },
            "products.csv":{
                "primary_key":"product_id",
                "description":"Product catalog"
            },
            "orders.csv":{
                "primary_key":"order_id",
                "description":"Products header records"
            },
            "order_items_csv":{
                "primary_key":"order_item_id",
                "description":"Products pruchased in each order"
            },
        
            "payments.csv":{
                "primary_key":"payment_id",
                "description":"Order payment records"
            },
            "returns.csv":{
                "primary_key":"returned_id",
                "description":"Returned order items"
            },
            "website_events.json":{
                "primary_key":"event_id",
                "description":"Website interaction events in JSON Lines format"
            }
        }
        dictionary_path=(
            BASE_DIR/"docs"/"data_dictionary.json"
        )
        dictionary_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )
        with open(
            dictionary_path,
            "w",
            encoding="utf-8"
        )as file:
            json.dump(
                data_dictionary,
                file,
                indent=4
            )
            print("\nAll datasets generated successfully.")
            print(f"Project directory:{BASE_DIR}")
if __name__=="__main__":
   main()

