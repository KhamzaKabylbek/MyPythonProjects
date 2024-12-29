import cv2


# Function to calculate and display the area of the object at the center
def calculate_and_display_area_at_center(contours, image):
    for contour in contours:
        area = cv2.contourArea(contour)

        # Calculate the centroid of the contour
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            # Draw the contour and the centroid
            cv2.drawContours(image, [contour], -1, (0, 255, 0), 2)
            cv2.circle(image, (cx, cy), 5, (255, 0, 0), -1)

            # Display the area at the center of the object
            cv2.putText(image, f'Area: {area}', (cx - 50, cy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


# Load the image
image_path = 'png-clipart-Стакан-table-glass-paşabahce-fizzy-drinks-glass.png'
image = cv2.imread(image_path)

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply GaussianBlur to reduce noise and help contour detection
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Use Canny edge detection to find edges in the image
edges = cv2.Canny(blurred, 50, 150)

# Find contours in the image
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Draw contours, calculate/display area, and display the result
calculate_and_display_area_at_center(contours, image)
cv2.imshow('Object Contours', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
