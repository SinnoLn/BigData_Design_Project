import pymongo
import pandas as pd
import matplotlib.pyplot as plt
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# MongoDB connection setup
try:
    client = pymongo.MongoClient("mongodb://localhost:27019/")
    logging.info("MongoDB client created.")

    # List database names to confirm connection
    db_names = client.list_database_names()
    logging.info("Databases: %s", db_names)

    # Check specific database and collection
    db = client["cycle"]
    collection_names = db.list_collection_names()
    logging.info("Collections in 'cycle' database: %s", collection_names)
except pymongo.errors.ServerSelectionTimeoutError as err:
    logging.error("Server selection timeout error: %s", err)
except pymongo.errors.ConnectionError as err:
    logging.error("Connection error: %s", err)
except Exception as err:
    logging.error("An error occurred: %s", err)

# If connection is successful, proceed with the analysis
if 'rental_info' in collection_names:
    # Start timer for overall execution
    start_time = time.time()

    # 쿼리 실행
    pipeline = [
        {
            "$lookup": {
                "from": "broken_history",
                "localField": "cycle_num",
                "foreignField": "cycle_num",
                "as": "faults"
            }
        },
        {
            "$group": {
                "_id": "$cycle_num",
                "totalRentals": {"$sum": 1},
                "totalFaults": {"$sum": {"$size": "$faults"}}
            }
        },
        {
            "$project": {
                "cycle_num": "$_id",
                "totalRentals": 1,
                "totalFaults": 1,
                "faultRate": {
                    "$cond": [{"$eq": ["$totalRentals", 0]}, 0, {"$divide": ["$totalFaults", "$totalRentals"]}]}
            }
        },
        {
            "$sort": {"faultRate": -1}
        }
    ]

    # Time the aggregation stage
    aggregation_start_time = time.time()
    try:
        results = list(db.rental_info.aggregate(pipeline))
        aggregation_end_time = time.time()
        logging.info("Aggregation time: {:.2f} seconds".format(aggregation_end_time - aggregation_start_time))

        # Convert results to DataFrame
        df_conversion_start_time = time.time()
        df = pd.DataFrame(results)
        df_conversion_end_time = time.time()
        logging.info(
            "DataFrame conversion time: {:.2f} seconds".format(df_conversion_end_time - df_conversion_start_time))

        # Visualization
        plt.figure(figsize=(10, 6))
        plt.bar(df['cycle_num'], df['faultRate'])
        plt.xlabel('Cycle Number')
        plt.ylabel('Fault Rate')
        plt.title('Bicycle Fault Rate Analysis')
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.show()

        # End timer for overall execution
        end_time = time.time()
        total_execution_time = end_time - start_time
        logging.info("Total execution time: {:.2f} seconds".format(total_execution_time))
    except pymongo.errors.OperationFailure as err:
        logging.error("Aggregation operation failed: %s", err)
    except Exception as err:
        logging.error("An error occurred during aggregation: %s", err)
else:
    logging.error("rental_info collection not found in the 'cycle' database.")