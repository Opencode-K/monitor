

import os
import argparse
import cv2

from app.services.detection_service import (
    detect_fire,
    detect_smoke,
    detect_temperature,
    detect_helmets
)

# Mapping of task names to detection functions
DETECT_MAP = {
    'fire': detect_fire,
    'smoke': detect_smoke,
    'temp': detect_temperature,
    'helmet': detect_helmets,
}


def process_image(input_path, detect_fn, output_dir, show):
    image = cv2.imread(input_path)
    if image is None:
        print(f"Failed to read {input_path}, skipping.")
        return

    annotated, detections = detect_fn(image)
    # Print detection results
    print(f"{os.path.basename(input_path)}: {detections}")

    # Save annotated image
    out_name = f"{detect_fn.__name__}_{os.path.basename(input_path)}"
    out_path = os.path.join(output_dir, out_name)
    cv2.imwrite(out_path, annotated)

    # Optionally display
    if show:
        cv2.imshow(f"{detect_fn.__name__} - {os.path.basename(input_path)}", annotated)
        key = cv2.waitKey(0)
        cv2.destroyAllWindows()
        if key == 27:
            exit(0)


def main():
    parser = argparse.ArgumentParser(
        description='Run detection model on images (file or directory) and visualize/save results'
    )
    parser.add_argument(
        '--task', choices=DETECT_MAP.keys(), required=True,
        help='Detection task: fire, smoke, temp, or helmet'
    )
    parser.add_argument(
        '--input', required=True,
        help='Input image file or directory containing images'
    )
    parser.add_argument(
        '--output-dir', default='output',
        help='Directory to save annotated output images'
    )
    parser.add_argument(
        '--show', action='store_true',
        help='Display each result image'
    )

    args = parser.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)

    detect_fn = DETECT_MAP[args.task]

    # Determine input paths
    input_paths = []
    if os.path.isfile(args.input):
        input_paths = [args.input]
    elif os.path.isdir(args.input):
        for filename in sorted(os.listdir(args.input)):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                input_paths.append(os.path.join(args.input, filename))
    else:
        print(f"Error: '{args.input}' is not a valid file or directory.")
        return

    # Process each image
    for path in input_paths:
        process_image(path, detect_fn, args.output_dir, args.show)


if __name__ == '__main__':
    main()

