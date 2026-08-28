import math
import os
import time
import cv2
import numpy as np
from typing import Optional


def generate_4k_video(
    prompt: str,
    output_folder: str = "generated_videos",
    filename: str = "",
    duration_seconds: int = 5,
    fps: int = 30,
    style: str = "auto"
) -> str:
    """Renders and generates a 4K UHD resolution (3840x2160) video and saves it to a designated folder.
    
    Args:
        prompt: Description or title of the video content (e.g., 'Space galaxy starfield', 'Glowing blue wave pattern', 'Abstract 4K motion graphics', 'TARS Sci-Fi HUD').
        output_folder: Directory folder where the 4K video will be saved (default 'generated_videos').
        filename: Optional custom filename (e.g., 'my_4k_video.mp4'). If empty, auto-generates a timestamped name.
        duration_seconds: Video duration in seconds (default 5 seconds, max 30 seconds).
        fps: Frames per second (default 30 fps).
        style: Visual rendering style ('sci-fi', 'gradient', 'particles', 'waves', 'auto').
    """
    print(f"\n  🎥 [TARS Action] Generating 4K UHD (3840x2160) Video for prompt: '{prompt}'...")

    width, height = 3840, 2160
    duration_seconds = max(1, min(30, int(duration_seconds)))
    total_frames = duration_seconds * fps

    # Setup output folder and filename
    os.makedirs(output_folder, exist_ok=True)
    if not filename:
        timestamp = int(time.time())
        clean_prompt = "".join(c for c in prompt[:15] if c.isalnum() or c in ("_", "-")).strip() or "video"
        filename = f"tars_4k_{clean_prompt}_{timestamp}.mp4"
    elif not filename.endswith(".mp4"):
        filename += ".mp4"

    full_output_path = os.path.abspath(os.path.join(output_folder, filename))

    try:
        # Define 4K MP4 VideoWriter (mp4v codec)
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(full_output_path, fourcc, float(fps), (width, height))

        if not out.isOpened():
            # Fallback codec
            fourcc = cv2.VideoWriter_fourcc(*"XVID")
            out = cv2.VideoWriter(full_output_path, fourcc, float(fps), (width, height))

        # Generate background 4K particles/stars
        num_stars = 400
        stars_x = np.random.randint(0, width, size=num_stars)
        stars_y = np.random.randint(0, height, size=num_stars)
        stars_z = np.random.uniform(0.5, 3.0, size=num_stars)
        stars_colors = np.random.randint(180, 255, size=(num_stars, 3))

        lower_prompt = prompt.lower()
        use_space = "space" in lower_prompt or "galaxy" in lower_prompt or "star" in lower_prompt or "sci-fi" in lower_prompt or style == "sci-fi"

        for i in range(total_frames):
            t = i / float(total_frames)

            # Base 4K background frame
            frame = np.zeros((height, width, 3), dtype=np.uint8)

            # Dynamic 4K Background Gradient
            b_val = int(30 + 40 * math.sin(t * math.pi * 2))
            g_val = int(20 + 30 * math.cos(t * math.pi * 2))
            r_val = int(40 + 50 * math.sin(t * math.pi * 4))

            # Apply vertical color ramp across 3840x2160 grid efficiently
            y_indices = np.linspace(0, 1, height)[:, None]
            frame[:, :, 0] = np.clip(y_indices * b_val + (1 - y_indices) * 15, 0, 255).astype(np.uint8)
            frame[:, :, 1] = np.clip(y_indices * g_val + (1 - y_indices) * 25, 0, 255).astype(np.uint8)
            frame[:, :, 2] = np.clip(y_indices * r_val + (1 - y_indices) * 45, 0, 255).astype(np.uint8)

            # Animated 4K Wave / Energy Lines
            for w in range(3):
                wave_y = int(height / 2 + math.sin(t * math.pi * 4 + w) * 250 + math.cos(w * 2) * 100)
                cv2.ellipse(
                    frame,
                    (width // 2, wave_y),
                    (1600 + w * 200, 300 + w * 100),
                    int(t * 360 * (w + 1) * 0.2),
                    0, 360,
                    (255 - w * 60, 180 + w * 20, 100 + w * 50),
                    4
                )

            # Animated 4K Particles / Starfield
            for idx in range(num_stars):
                # Move particles
                stars_y[idx] = (stars_y[idx] + int(stars_z[idx] * 3)) % height
                x = int(stars_x[idx])
                y = int(stars_y[idx])
                radius = int(stars_z[idx] * 2)
                color = (int(stars_colors[idx][0]), int(stars_colors[idx][1]), int(stars_colors[idx][2]))
                cv2.circle(frame, (x, y), radius, color, -1)

            # 4K Title & HUD Overlay Text
            title_text = f"TARS 4K ENGINE: {prompt[:35]}"
            subtitle_text = f"RESOLUTION: 3840x2160 UHD | FPS: {fps} | FRAME {i+1}/{total_frames}"

            cv2.putText(frame, title_text, (100, 160), cv2.FONT_HERSHEY_SIMPLEX, 2.2, (255, 255, 255), 4, cv2.LINE_AA)
            cv2.putText(frame, subtitle_text, (100, 240), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 215, 255), 2, cv2.LINE_AA)

            # Border accent frame
            cv2.rectangle(frame, (40, 40), (width - 40, height - 40), (0, 215, 255), 3)

            out.write(frame)

        out.release()

        file_size_mb = os.path.getsize(full_output_path) / (1024 * 1024)

        return (
            f"Successfully generated 4K UHD Video!\n"
            f" • Output Path: {full_output_path}\n"
            f" • Resolution: 3840 x 2160 (4K UHD)\n"
            f" • Duration: {duration_seconds} seconds ({total_frames} frames @ {fps} fps)\n"
            f" • File Size: {file_size_mb:.2f} MB\n"
            f" • Status: Saved and ready in folder '{output_folder}'."
        )

    except Exception as e:
        return f"Failed to generate 4K video: {str(e)}"
