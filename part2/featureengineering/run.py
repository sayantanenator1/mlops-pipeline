import os
import argparse
import logging
import pandas as pd
import pickle
import gcsfs

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Set up argument parser
parser = argparse.ArgumentParser()
parser.add_argument("--validated_train_path",
                    type=str,
                    help="Path to validated train file")
parser.add_argument("--feature_store_path",
                    type=str,
                    help="Path to feature store base directory")

def load_gcs(gcs_path, arr):
    logging.debug(f"Saving to GCS path: {gcs_path}")
    fs = gcsfs.GCSFileSystem(project='alien-vim-449103-n5')
    with fs.open(gcs_path, 'wb') as f:
        f.write(pickle.dumps(arr))
    logging.debug(f"Successfully saved to {gcs_path}")

def main(args):
    logging.info("Reading validated data")
    df = pd.read_csv(args.validated_train_path)
    
    # Verify data
    logging.debug(f"DataFrame shape: {df.shape}")
    
    X = df.drop(['id', 'booking_status'], axis=1).values
    y = df['booking_status'].values
    
    logging.debug(f"X shape: {X.shape}, y shape: {y.shape}")
    
    # Save data to GCS
    load_gcs(os.path.join(args.feature_store_path, "X.npy"), X)
    load_gcs(os.path.join(args.feature_store_path, "y.npy"), y)
    
    logging.info("Saved data engineered artifacts")

if __name__ == "__main__":
    args = parser.parse_args()
    main(args)

