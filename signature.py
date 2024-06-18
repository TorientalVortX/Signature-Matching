import cv2
from skimage.metrics import structural_similarity as ssim

# TODO: Add contour detection for enhanced accuracy

def match(path1, path2):
    """
    Compares two images for similarity using Structural Similarity Index (SSIM).
    
    Parameters:
    - path1: str, path to the first image file
    - path2: str, path to the second image file
    
    Returns:
    - similarity_value: float, percentage of similarity between the two images
    """
    # Read the images from the given file paths
    img1 = cv2.imread(path1)
    img2 = cv2.imread(path2)

    # Convert the images to grayscale
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Resize the images to a fixed size for comparison
    img1 = cv2.resize(img1, (300, 300))
    img2 = cv2.resize(img2, (300, 300))

    # Display both images (for visual verification)
    cv2.imshow("Image 1", img1)
    cv2.imshow("Image 2", img2)
    cv2.waitKey(0)  # Wait for a key press to close the displayed images
    cv2.destroyAllWindows()

    # Calculate the Structural Similarity Index (SSIM) between the two images
    similarity_value = "{:.2f}".format(ssim(img1, img2) * 100)

    return float(similarity_value)

# Example usage
# ans = match("D:\\Code\\Git stuff\\Signature-Matching\\assets\\1.png",
#             "D:\\Code\\Git stuff\\Signature-Matching\\assets\\3.png")
# print(ans)
# print(type(ans))
