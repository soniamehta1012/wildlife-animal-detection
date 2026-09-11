# Wildlife Animal Detection – Frontend

## Frontend Overview

The frontend provides a simple and user-friendly interface for detecting wildlife animals from uploaded images. Users can upload an animal image, request a prediction, view the detection result, and access their previous prediction history.

## Frontend Flow

```text
Home Page
    ↓
Upload Animal Image
    ↓
Preview Uploaded Image
    ↓
Click "Predict Animal"
    ↓
Animal Detection / Prediction
    ↓
Display Prediction Result
    ↓
Store Prediction in History
    ↓
View Previous Predictions in History
```

## Step-by-Step User Flow

### 1. Home Page

The application starts with the Home page.

The Home page contains:

* Website title and introduction
* Navigation bar
* Image upload section
* Image preview area
* **Predict Animal** button
* Access to the History section

### 2. Upload Animal Image

The user can upload an image of a wildlife animal.

The frontend provides:

* Image selection from the device
* Drag-and-drop upload option
* Uploaded image preview
* Image validation before prediction

The selected image is displayed on the page so that the user can verify it before starting the prediction.

### 3. Predict Animal

After uploading the image, the user clicks the **Predict Animal** button.

The frontend then sends the selected image for animal detection/prediction.

```text
Uploaded Image
      ↓
Predict Animal Button
      ↓
Send Image for Detection
```

### 4. Display Prediction Result

After the prediction is completed, the frontend displays the result to the user.

The result section can contain:

* Detected animal name
* Prediction confidence
* Uploaded image
* Prediction status/result message

Example:

```text
┌─────────────────────────────┐
│       Prediction Result     │
├─────────────────────────────┤
│                             │
│        [Animal Image]       │
│                             │
│  Detected Animal: Tiger     │
│  Confidence: 94%            │
│                             │
└─────────────────────────────┘
```

### 5. Store Prediction in History

After a successful prediction, the prediction details are stored in the application's history.

Each history entry can contain:

* Uploaded animal image
* Detected animal name
* Confidence score
* Date and time of prediction

```text
Prediction Completed
        ↓
Save Prediction Details
        ↓
Add Entry to History
```

### 6. View History

The **History** section allows users to view their previous animal detection results.

The history page displays previous predictions in an organized format.


┌──────────────────────────────────┐
│            History               │
├──────────────────────────────────┤
│ [Image]  Tiger      94%          │
│          Date/Time               │
├──────────────────────────────────┤
│ [Image]  Lion       96%          │
│          Date/Time               │
└──────────────────────────────────┘


## Complete Frontend Workflow


                 ┌───────────────┐
                 │   Home Page   │
                 └───────┬───────┘
                         ↓
                 ┌───────────────┐
                 │ Upload Image  │
                 └───────┬───────┘
                         ↓
                 ┌───────────────┐
                 │ Image Preview │
                 └───────┬───────┘
                         ↓
                 ┌───────────────┐
                 │ Predict Animal│
                 └───────┬───────┘
                         ↓
                 ┌───────────────┐
                 │    Result     │
                 │ Animal +      │
                 │ Confidence    │
                 └───────┬───────┘
                         ↓
                 ┌───────────────┐
                 │ Store History │
                 └───────┬───────┘
                         ↓
                 ┌───────────────┐
                 │History Section│
                 └───────────────┘




## Frontend Objective

The frontend is designed to provide a smooth flow:

**Upload → Preview → Predict → Display Result → Store → View History**

This structure keeps the wildlife detection process simple and understandable for the user while providing a clear interface for interacting with the animal detection system.
