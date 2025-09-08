# Object Dimension Measurement Tool

A web-based application to capture or upload images, process them to detect objects, and measure their dimensions in millimeters. Built with Flask and OpenCV, it provides an intuitive interface for real-time or uploaded image analysis.

---

## Features

- Capture images directly from your webcam
- Upload images for processing
- Adjust processing parameters:
  - Threshold
  - Blur amount
  - Pixel-to-mm ratio
- Visualize original and processed images
- Automatic measurement of object diameter, categorization, and pixel radius
- Results displayed in a user-friendly dashboard

---

## Procedure
<img width="880" height="664" alt="Screenshot 2025-09-08 at 12 06 45 pm" src="https://github.com/user-attachments/assets/64ee84f3-eb31-450e-ad0c-32af4bfc6b0c" />
Start the camera and capture an image

<img width="879" height="201" alt="Screenshot 2025-09-08 at 12 06 38 pm" src="https://github.com/user-attachments/assets/d610f891-e89f-40b5-8cf1-e3593b2b07d3" />
Change Threshold, Blur Amount and Pixel to MM Ratio and click Process Image


---
# Result

<img width="878" height="589" alt="Screenshot 2025-09-08 at 12 06 29 pm" src="https://github.com/user-attachments/assets/f313a000-e687-452c-9902-e869df3a2240" />

---

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone <repository_url>
cd object-dimension-measurement
