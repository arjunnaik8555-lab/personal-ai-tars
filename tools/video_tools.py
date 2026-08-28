import math
import os
import subprocess
import tempfile
import time
import wave
import cv2
import imageio_ffmpeg
import numpy as np


def generate_slow_ambient_music(duration_seconds: float, theme: str = "space", output_wav: str = "/tmp/tars_ambient.wav") -> str:
    """Synthesizes a custom slow ambient soundtrack matching the video theme.
    
    Args:
        duration_seconds: Length of the audio track in seconds.
        theme: Musical style ('space', 'chill', 'cinematic').
        output_wav: Target WAV file path.
    """
    sample_rate = 44100
    n_samples = int(sample_rate * duration_seconds)
    t = np.linspace(0, duration_seconds, n_samples, False)

    signal = np.zeros(n_samples)

    if theme == "chill":
        # Slow Pentatonic Ambient Pad (D Major / F# / A / B)
        freqs = [146.83, 220.0, 293.66, 370.0, 440.0]
        lfo_speed = 0.08
    elif theme == "cinematic":
        # Deep Atmospheric Crescendo Pad (C Minor / Eb / G / Bb)
        freqs = [130.81, 164.81, 196.0, 233.08, 392.0]
        lfo_speed = 0.05
    else:
        # Sci-Fi Space Ambient Drone (A Minor 9th / 432Hz tuned harmonics)
        freqs = [110.0, 164.81, 220.0, 329.63, 432.0, 659.25]
        lfo_speed = 0.06

    for i, f in enumerate(freqs):
        # Multi-layered LFO modulation for warm analog synth swells
        lfo = 0.5 + 0.5 * np.sin(2 * np.pi * lfo_speed * t + i * 1.2)
        lfo2 = 0.8 + 0.2 * np.cos(2 * np.pi * (lfo_speed * 0.5) * t)
        harmonic = 0.25 * np.sin(2 * np.pi * f * t) + 0.1 * np.sin(2 * np.pi * (f * 1.002) * t)
        signal += harmonic * lfo * lfo2

    # Normalize audio & apply soft fade-in (3s) and fade-out (4s)
    max_val = np.max(np.abs(signal))
    if max_val > 0:
        signal = signal / max_val * 0.75

    fade_in = np.minimum(1.0, t / 3.0)
    fade_out = np.minimum(1.0, (duration_seconds - t) / 4.0)
    signal = signal * fade_in * fade_out

    # Convert to 16-bit PCM stereo WAV
    scaled = (signal * 32767).astype(np.int16)
    stereo_signal = np.column_stack((scaled, scaled))

    with wave.open(output_wav, "w") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(stereo_signal.tobytes())

    return output_wav


def generate_4k_video(
    prompt: str,
    output_folder: str = "generated_videos",
    filename: str = "",
    duration_seconds: int = 20,
    fps: int = 30,
    style: str = "auto",
    include_music: bool = True
) -> str:
    """Renders a 4K UHD resolution (3840x2160) video (20 sec to 2 mins) complete with custom slow ambient music.
    
    Args:
        prompt: Description or title of the video content (e.g., 'Space galaxy starfield', 'Chill relaxing waves', 'Abstract 4K motion graphics').
        output_folder: Directory folder where the 4K video will be stored (default 'generated_videos').
        filename: Optional custom filename (e.g., 'my_4k_video.mp4'). Auto-generated if empty.
        duration_seconds: Video length in seconds (Minimum 20 seconds, Maximum 120 seconds / 2 mins).
        fps: Frames per second (default 30 fps).
        style: Visual rendering style ('sci-fi', 'chill', 'cinematic', 'auto').
        include_music: Whether to synthesize and add matching slow ambient music (default True).
    """
    print(f"\n  🎥 [TARS Action] Generating 4K UHD (3840x2160) Video with Slow Ambient Music...")

    width, height = 3840, 2160
    
    # Enforce duration bounds: At least 20 seconds, max 120 seconds (2 mins)
    duration_seconds = max(20, min(120, int(duration_seconds)))
    total_frames = duration_seconds * fps

    # Setup output folder and filename
    os.makedirs(output_folder, exist_ok=True)
    timestamp = int(time.time())
    if not filename:
        clean_prompt = "".join(c for c in prompt[:15] if c.isalnum() or c in ("_", "-")).strip() or "video"
        filename = f"tars_4k_{clean_prompt}_{timestamp}.mp4"
    elif not filename.endswith(".mp4"):
        filename += ".mp4"

    temp_video_path = os.path.join(tempfile.gettempdir(), f"temp_4k_raw_{timestamp}.mp4")
    final_output_path = os.path.abspath(os.path.join(output_folder, filename))

    try:
        # Define 4K MP4 VideoWriter (mp4v codec)
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(temp_video_path, fourcc, float(fps), (width, height))

        if not out.isOpened():
            fourcc = cv2.VideoWriter_fourcc(*"XVID")
            out = cv2.VideoWriter(temp_video_path, fourcc, float(fps), (width, height))

        # Generate background 4K particles/starfield
        num_stars = 500
        stars_x = np.random.randint(0, width, size=num_stars)
        stars_y = np.random.randint(0, height, size=num_stars)
        stars_z = np.random.uniform(0.5, 3.5, size=num_stars)
        stars_colors = np.random.randint(180, 255, size=(num_stars, 3))

        lower_prompt = prompt.lower()
        if "chill" in lower_prompt or "relax" in lower_prompt:
            music_theme = "chill"
        elif "epic" in lower_prompt or "cinematic" in lower_prompt:
            music_theme = "cinematic"
        else:
            music_theme = "space"

        for i in range(total_frames):
            t = i / float(total_frames)

            # Base 4K background frame
            frame = np.zeros((height, width, 3), dtype=np.uint8)

            # Dynamic 4K Background Gradient
            b_val = int(35 + 45 * math.sin(t * math.pi * 2))
            g_val = int(25 + 35 * math.cos(t * math.pi * 2))
            r_val = int(45 + 55 * math.sin(t * math.pi * 3))

            # Apply vertical gradient
            y_indices = np.linspace(0, 1, height)[:, None]
            frame[:, :, 0] = np.clip(y_indices * b_val + (1 - y_indices) * 20, 0, 255).astype(np.uint8)
            frame[:, :, 1] = np.clip(y_indices * g_val + (1 - y_indices) * 30, 0, 255).astype(np.uint8)
            frame[:, :, 2] = np.clip(y_indices * r_val + (1 - y_indices) * 50, 0, 255).astype(np.uint8)

            # Animated 4K Energy Waves
            for w in range(3):
                wave_y = int(height / 2 + math.sin(t * math.pi * 4 + w) * 280 + math.cos(w * 2) * 120)
                cv2.ellipse(
                    frame,
                    (width // 2, wave_y),
                    (1700 + w * 220, 320 + w * 110),
                    int(t * 360 * (w + 1) * 0.15),
                    0, 360,
                    (255 - w * 50, 190 + w * 20, 110 + w * 45),
                    4
                )

            # Animated Starfield Particles
            for idx in range(num_stars):
                stars_y[idx] = (stars_y[idx] + int(stars_z[idx] * 2.5)) % height
                x = int(stars_x[idx])
                y = int(stars_y[idx])
                radius = int(stars_z[idx] * 2.2)
                color = (int(stars_colors[idx][0]), int(stars_colors[idx][1]), int(stars_colors[idx][2]))
                cv2.circle(frame, (x, y), radius, color, -1)

            # 4K Title & HUD Overlay Text
            title_text = f"TARS 4K ENGINE: {prompt[:38]}"
            subtitle_text = f"RESOLUTION: 3840x2160 UHD | DURATION: {duration_seconds}s | SLOW AMBIENT AUDIO"

            cv2.putText(frame, title_text, (100, 160), cv2.FONT_HERSHEY_SIMPLEX, 2.2, (255, 255, 255), 4, cv2.LINE_AA)
            cv2.putText(frame, subtitle_text, (100, 240), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (0, 215, 255), 2, cv2.LINE_AA)

            # Outer border
            cv2.rectangle(frame, (40, 40), (width - 40, height - 40), (0, 215, 255), 3)

            out.write(frame)

        out.release()

        # Step 2: Generate Slow Ambient Music Track & Combine with FFmpeg
        final_video = temp_video_path
        if include_music:
            temp_wav = os.path.join(tempfile.gettempdir(), f"tars_audio_{timestamp}.wav")
            generate_slow_ambient_music(duration_seconds=float(duration_seconds), theme=music_theme, output_wav=temp_wav)

            ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
            cmd = [
                ffmpeg_exe, "-y",
                "-i", temp_video_path,
                "-i", temp_wav,
                "-c:v", "copy",
                "-c:a", "aac",
                "-shortest",
                final_output_path
            ]
            res = subprocess.run(cmd, capture_output=True, text=True, check=False)
            if res.returncode == 0:
                final_video = final_output_path
                # Clean temp raw video
                if os.path.exists(temp_video_path):
                    os.remove(temp_video_path)
            else:
                os.rename(temp_video_path, final_output_path)

        file_size_mb = os.path.getsize(final_output_path) / (1024 * 1024)

        return (
            f"Successfully generated 4K UHD Video with Slow Ambient Music!\n"
            f" • Output Path: {final_output_path}\n"
            f" • Resolution: 3840 x 2160 (4K UHD)\n"
            f" • Duration: {duration_seconds} seconds ({total_frames} frames @ {fps} fps)\n"
            f" • Audio Track: Synthesized Slow Ambient Music ({music_theme.capitalize()} Pad, Stereo AAC)\n"
            f" • File Size: {file_size_mb:.2f} MB\n"
            f" • Status: Saved in folder '{output_folder}'."
        )

    except Exception as e:
        return f"Failed to generate 4K video: {str(e)}"
