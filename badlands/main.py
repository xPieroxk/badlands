import os
import matplotlib.pyplot as plt
import config
import numpy as np
import rasterio
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, jaccard_score, balanced_accuracy_score
)

tif_files = [f for f in os.listdir(config.FEATURES_FOLDER)]

# Define number of columns and rows
n_cols = 3
n_rows = -(-len(tif_files) // n_cols)

fig, axes = plt.subplots(n_rows, n_cols, figsize=(5 * n_cols, 5 * n_rows))
axes = axes.flatten()

for i, tif in enumerate(tif_files):
    tif_path = os.path.join(config.FEATURES_FOLDER, tif)
    with rasterio.open(tif_path) as src:
        img = src.read(1)  # Read first band
        axes[i].imshow(img, cmap="gray")
        axes[i].set_title(tif)
        axes[i].axis("off")

# Hide unused subplots if any
for j in range(i + 1, len(axes)):
    axes[j].axis("off")

plt.tight_layout()
plt.show()

'''
tif_path = os.path.join(config.FEATURES_FOLDER, '')

with rasterio.open(tif_path) as src:
    img = src.read(1)  # Read first band

plt.figure(figsize=(6, 6))
plt.imshow(img, cmap="gray")
plt.title(filename)
plt.axis("off")
plt.show()
'''
ground_truth = os.path.join(config.FEATURES_FOLDER, 'badlands_mask.tif')
final_mask = os.path.join(config.FEATURES_FOLDER, 'final_mask.tif')

# Load ground truth mask
with rasterio.open(ground_truth) as src:
    ground_truth = src.read(1).astype(np.uint8).flatten()

# Load final mask
with rasterio.open(final_mask) as src:
    final_mask = src.read(1).astype(np.uint8).flatten()

# Compute metrics
accuracy = accuracy_score(ground_truth, final_mask)
precision = precision_score(ground_truth, final_mask)
recall = recall_score(ground_truth, final_mask)
f1 = f1_score(ground_truth, final_mask)
iou = jaccard_score(ground_truth, final_mask)
dice = 2 * iou / (1 + iou)
specificity = recall_score(ground_truth, final_mask, pos_label=0)
balanced_acc = balanced_accuracy_score(ground_truth, final_mask)

print(f"Accuracy: {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1 Score: {f1:.4f}")
print(f"IoU: {iou:.4f}")
print(f"Dice Coefficient: {dice:.4f}")
print(f"Specificity: {specificity:.4f}")
print(f"Balanced Accuracy: {balanced_acc:.4f}")
