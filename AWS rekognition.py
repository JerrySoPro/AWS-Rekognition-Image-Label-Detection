#Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-developer-guide/blob/master/LICENSE-SAMPLECODE.)

import boto3

def get_all_images_from_bucket(bucket):
    """Get all image files from the S3 bucket"""
    s3_client = boto3.client('s3', region_name='us-east-1')
    
    try:
        response = s3_client.list_objects_v2(Bucket=bucket)
        
        if 'Contents' not in response:
            print(f"No objects found in bucket: {bucket}")
            return []
        
        # AWS Rekognition only supports JPEG and PNG
        image_extensions = ('.jpg', '.jpeg', '.png')
        images = [obj['Key'] for obj in response['Contents'] 
                  if obj['Key'].lower().endswith(image_extensions)]
        
        return images
    except Exception as e:
        print(f"Error listing bucket contents: {e}")
        return []

def detect_labels(photo, bucket):

    client=boto3.client('rekognition', region_name='us-east-1')

    try:
        response = client.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':photo}},
            MaxLabels=5)

        print('Detected labels for ' + photo) 
        print()   
        for label in response['Labels']:
            print ("Label: " + label['Name'])
            print ("Confidence: " + str(label['Confidence']))
            print ("Instances:")
            for instance in label['Instances']:
                print ("  Bounding box")
                print ("    Top: " + str(instance['BoundingBox']['Top']))
                print ("    Left: " + str(instance['BoundingBox']['Left']))
                print ("    Width: " +  str(instance['BoundingBox']['Width']))
                print ("    Height: " +  str(instance['BoundingBox']['Height']))
                print ("  Confidence: " + str(instance['Confidence']))
                print()

            print ("Parents:")
            for parent in label['Parents']:
                print ("   " + parent['Name'])
            print ("----------")
            print ()
        return len(response['Labels'])
    
    except Exception as e:
        print(f"ERROR processing {photo}: {e}")
        print()
        return 0


def main():
    bucket='project-rekognition-s3'
    
    # Get all images from bucket
    print(f"Fetching images from bucket: {bucket}")
    images = get_all_images_from_bucket(bucket)
    
    if not images:
        print("No images found in the bucket.")
        return
    
    print(f"Found {len(images)} image(s) in the bucket")
    print(f"Files: {', '.join(images)}")
    print("=" * 60)
    
    # Process each image
    total_labels = 0
    successful = 0
    failed = 0
    
    for photo in images:
        print(f"\n{'=' * 60}")
        label_count = detect_labels(photo, bucket)
        total_labels += label_count
        
        if label_count > 0:
            successful += 1
            print(f"✓ Labels detected in {photo}: {label_count}")
        else:
            failed += 1
            print(f"✗ Failed to process {photo}")
        print("=" * 60)
    
    print(f"\n\n{'=' * 60}")
    print(f"SUMMARY")
    print(f"{'=' * 60}")
    print(f"Total images found: {len(images)}")
    print(f"Successfully processed: {successful}")
    print(f"Failed: {failed}")
    print(f"Total labels detected: {total_labels}")


if __name__ == "__main__":
    main()
