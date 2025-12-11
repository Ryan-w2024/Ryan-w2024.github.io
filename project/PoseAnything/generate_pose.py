import os
import json
import webbrowser

# --- 配置区域 ---

VIDEOS_ROOT_DIR = 'pose'
OUTPUT_HTML_FILE = 'poseanything.html'
ANNOTATIONS_JSON_PATH = 'anno.json'

PAGE_TITLE = "PoseAnything: Universal Pose-guided Video Generation with Part-aware Temporal Coherence"
PAGE_INTRODUCTION = (
    "On this page, we present a demo video and detailed comparative results showcasing the performance of our method against state-of-the-art controllable video generation approaches. We conduct the comparative experiments on data from two distinct domains: human and non-human, highlighting our model's generalization across diverse subject categories."
)

SECTIONS_CONFIG = [
    {
        'title': 'Demo Video',
        'description': '',
        'folder': 'demo',  # demo 文件夹，视频放 pose/demo 下
        'videos_per_row': 1,
        'is_comparison': False,
    },
    {
        'title': 'Human Data Comparison',
        'description': 'This section provides comparison with state-of-the-art methods on human data. Each row corresponds to a single test case with same input. Our model achieves excellent continuity in motion, consistent appearance, and stable background, while current SOTA methods show distortion in key areas like the hands and face.',
        'folder': 'tiktok',
        'videos_per_row': 6,
        'is_comparison': True,
        'methods': [
            {'folder': 'gt', 'name': 'GT'},
            {'folder': 'skeleton', 'name': 'Pose'},
            {'folder': 'Ours', 'name': 'Ours'},
            {'folder': 'Unianimate', 'name': 'UniAnimate'},
            {'folder': 'Animate-X', 'name': 'Animate-X'},
            {'folder': 'magicpose', 'name': 'MagicPose'}
        ]
    },
    {
        'title': 'Non-Human Data Comparison',
        'description': 'This section provides comparison with state-of-the-art methods on non-human data. Each row corresponds to a single test case. Since ATI, SG-I2V, and Tora are trajectory-guided video generation methods, we manually constructed the input control information for Tora and SG-I2V, and utilized ATI\'s self-proposed control information extraction mechanism for its input. \
            Furthermore, given that the default generation frame count of SG-I2V and Tora are less than the default 81, used by our PoseAnything and ATI methods, we align the frame count of all videos to 81 frames by duplicating the last frame to ensure a intuitive comparison.\
            The results indicate that our PoseAnything model demonstrates a significant advantage in precise pose control, whereas competing methods struggle to achieve frame-level pose alignment and tend to generate hallucinations during large-range motion synthesis.',
        'folder': 'non-human',
        'videos_per_row': 6,
        'is_comparison': True,
        'methods': [
            {'folder': 'gt', 'name': 'GT'},
            {'folder': 'skeleton', 'name': 'Pose'},
            {'folder': 'ours', 'name': 'Ours'},
            {'folder': 'ATI', 'name': 'ATI'},
            {'folder': 'SG-I2V', 'name': 'SG-I2V'},
            {'folder': 'tora', 'name': 'Tora'}
        ]
    },
]

def get_video_files(directory):
    """获取指定目录下的所有视频文件，并按名称排序"""
    if not os.path.isdir(directory):
        return []
    supported_formats = ('.mp4', '.webm', '.mov', '.ogg')
    files = [f for f in os.listdir(directory) if f.lower().endswith(supported_formats)]
    files.sort()
    return files

def create_video_element(video_path, folder_name, annotations, override_description=None, video_ratio_class="video-fixed-ratio"):
    """
    为单个视频创建HTML代码块。
    """
    if override_description:
        description = override_description
    else:
        base_filename = os.path.splitext(os.path.basename(video_path))[0]
        description = annotations.get(base_filename, base_filename)

    return f'''
            <div class="video-container">
                <video class="{video_ratio_class}" controls muted loop>
                    <source src="{video_path}" type="video/mp4">
                </video>
                <p>{description}</p>
            </div>'''

def generate_html(annotations):
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale-1.0">
    <title>Supplementary Materials</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 0 auto; max-width: 1200px; padding: 20px; color: #333; }}
        h1 {{ text-align: center; }}
        h2 {{
            text-align: center; /* 确保 H2 文字居中 */
            border-bottom: 2px solid #ccc; 
            padding-bottom: 10px; 
            margin-top: 40px; 
        }}
        .intro {{ text-align: left; margin-bottom: 40px; font-size: 1.1em; line-height: 1.6; }}
        .section-description {{ font-size: 0.95em; color: #555; margin-top: -5px; margin-bottom: 25px; }}
        .comparison-prompt {{
            width: 100%;
            text-align: center;
            font-weight: bold;
            font-size: 1.1em;
            margin-top: 30px;
            margin-bottom: 5px;
            padding: 0 10px;
            box-sizing: border-box;
        }}
        .video-section {{ margin-bottom: 30px; }}

        .video-row,
        .video-row-2-center,
        .video-row-4-center {{
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            margin: 0;
            align-items: flex-start;
            justify-content: center;
        }}
        .video-row-2-center {{ flex-direction: row; margin-bottom: 10px; }}
        .video-row-4-center {{ flex-direction: row; }}
        .video-container {{
            flex: 1 0 0;
            margin: 0;
            box-sizing: border-box;
            text-align: center;
            display: flex;
            flex-direction: column;
            max-width: 180px;
        }}
        .video-fixed-ratio {{ width: 100%; aspect-ratio: 2 / 3; object-fit: contain; background-color: #000; border: 1px solid #ddd; }}
        .video-auto-ratio {{ width: 100%; height: auto; object-fit: contain; background-color: #000; border: 1px solid #ddd; }}
        .video-square-ratio {{ width: 100%; aspect-ratio: 1 / 1; object-fit: contain; background-color: #000; border: 1px solid #ddd; }}
        .video-portrait-ratio {{ width: 100%; aspect-ratio: 16 / 9; object-fit: contain; background-color: #000; border: 1px solid #ddd; }}
        .video-original-size {{ max-width: 100%; height: auto; object-fit: contain; background-color: #000; border: 1px solid #ddd; }}
        .video-container p {{ margin-top: 8px; font-size: 14px; color: #555; word-wrap: break-word; }}

        .non-human-section .video-container {{ max-width: 320px !important; }}
        .non-human-section .video-portrait-ratio {{ max-width: 320px !important; }}

        /* 只控制 Demo Video 的宽度 */
        .demo-section .video-container {{
            max-width: 800px;
            margin: 0 auto;
        }}

        .demo-section .video-original-size {{
            width: 100%;
            aspect-ratio: 16 / 9;
            object-fit: cover;
            display: block;
            background: #000;
        }}

        .play-row-btn {{
            display: inline-block;
            margin-bottom: 10px;
            background: #6c757d; /* 灰色背景 (Bootstrap secondary color) */
            color: #ffffff; /* 白色文本 */
            border: none;
            border-radius: 4px;
            padding: 5px 18px;
            cursor: pointer;
            font-size: 15px;
            transition: background 0.2s ease; /* 添加平滑过渡 */
        }}
        .play-row-btn:hover {{ 
            background: #495057; /* 悬停时深灰色 */
        }}
    </style>
    <script>
        // 播放某一行所有视频
        function playRow(rowId) {{
            var row = document.getElementById(rowId);
            if (row) {{
                var videos = row.getElementsByTagName('video');
                for (let i = 0; i < videos.length; i++) {{
                    try {{
                        videos[i].currentTime = 0; // 从头播放
                        videos[i].play();
                    }} catch(e) {{}}
                }}
            }}
        }}
        // 播放多行
        function playRows(rowIds) {{
            for (var idx=0; idx<rowIds.length; idx++) {{
                playRow(rowIds[idx]);
            }}
        }}
    </script>
</head>
<body>
    <h1>{PAGE_TITLE}</h1>
    <p class="intro">{PAGE_INTRODUCTION}</p>
'''

    row_uid_counter = 0  # 用于唯一id

    for section in SECTIONS_CONFIG:
        if section.get('is_comparison'):
            base_section_dir = os.path.join(VIDEOS_ROOT_DIR, section['folder'])
            methods = section.get('methods', [])
            if not os.path.isdir(base_section_dir) or not methods:
                continue

            all_video_files = set()
            for method in methods:
                method_dir = os.path.join(base_section_dir, method['folder'])
                video_files_for_method = get_video_files(method_dir)
                all_video_files.update(video_files_for_method)
            sorted_cases = sorted(list(all_video_files))

            html_content += f'''
    <div class="video-section">
        <h2>{section['title']}</h2>'''
            if section.get('description'):
                html_content += f'\n        <p class="section-description">{section["description"]}</p>'

            for i, case_filename in enumerate(sorted_cases):
                base_filename = os.path.splitext(case_filename)[0]
                prompt_text = annotations.get(base_filename, f"Case {i+1}")
                html_content += f'\n        <p class="comparison-prompt">{prompt_text}</p>'

                # Human Data Comparison: 一行一个按钮
                if section['title'] == 'Human Data Comparison':
                    row_uid_counter += 1
                    row_id = f"video-row-human-{row_uid_counter}"
                    # 比较部分保留按钮
                    html_content += f'\n        <button class="play-row-btn" onclick="playRow(\'{row_id}\')">▶ Play All Videos in Row</button>'
                    html_content += f'\n        <div class="video-row" id="{row_id}">'
                    for method in methods:
                        video_path = os.path.join(base_section_dir, method['folder'], case_filename)
                        video_path_url = video_path.replace(os.sep, "/")
                        if os.path.exists(video_path):
                            html_content += create_video_element(
                                video_path_url, section['folder'], annotations,
                                override_description=method['name'],
                                video_ratio_class="video-square-ratio"
                            )
                        else:
                            html_content += f'''
            <div class="video-container">
                <div class="video-square-ratio" style="background-color: #f0f0f0; display: flex; align-items: center; justify-content: center; color: #999;">Not Available</div>
                <p>{method['name']}</p>
            </div>'''
                    html_content += '\n        </div>'

                # Non-Human Data Comparison: 两行共用一个按钮
                elif section['title'] == 'Non-Human Data Comparison':
                    # 前2个
                    row_uid_counter += 1
                    row_id2 = f"video-row-nonhuman-2-{row_uid_counter}"
                    # 后4个
                    row_uid_counter += 1
                    row_id4 = f"video-row-nonhuman-4-{row_uid_counter}"
                    html_content += f'\n    <div class="non-human-section">'
                    # 比较部分保留按钮
                    html_content += f'\n        <button class="play-row-btn" onclick="playRows([\'{row_id2}\',\'{row_id4}\'])">▶ Play All Videos in Row</button>'
                    # 前2个视频
                    html_content += f'\n        <div class="video-row-2-center" id="{row_id2}">'
                    for method in methods[:2]:
                        video_path = os.path.join(base_section_dir, method['folder'], case_filename)
                        video_path_url = video_path.replace(os.sep, "/")
                        if os.path.exists(video_path):
                            html_content += create_video_element(
                                video_path_url, section['folder'], annotations,
                                override_description=method['name'],
                                video_ratio_class="video-portrait-ratio"
                            )
                        else:
                            html_content += f'''
            <div class="video-container">
                <div class="video-portrait-ratio" style="background-color: #f0f0f0; display: flex; align-items: center; justify-content: center; color: #999;">Not Available</div>
                <p>{method['name']}</p>
            </div>'''
                    html_content += '\n        </div>'

                    # 后4个视频
                    html_content += f'\n        <div class="video-row-4-center" id="{row_id4}">'
                    for method in methods[2:]:
                        video_path = os.path.join(base_section_dir, method['folder'], case_filename)
                        video_path_url = video_path.replace(os.sep, "/")
                        if os.path.exists(video_path):
                            html_content += create_video_element(
                                video_path_url, section['folder'], annotations,
                                override_description=method['name'],
                                video_ratio_class="video-portrait-ratio"
                            )
                        else:
                            html_content += f'''
            <div class="video-container">
                <div class="video-portrait-ratio" style="background-color: #f0f0f0; display: flex; align-items: center; justify-content: center; color: #999;">Not Available</div>
                <p>{method['name']}</p>
            </div>'''
                    html_content += '\n        </div>'
                    html_content += '\n    </div>'  # 关闭non-human部分

            html_content += '\n    </div>'

        else:
            section_dir = os.path.join(VIDEOS_ROOT_DIR, section['folder'])
            video_files = get_video_files(section_dir)
            if not video_files: continue

            # ----------- 关键修改：为 Demo Video 区块加 demo-section class ------------
            if section['title'] == 'Demo Video':
                html_content += f'''
    <div class="video-section demo-section">
        <h2>{section['title']}</h2>'''
            else:
                html_content += f'''
    <div class="video-section">
        <h2>{section['title']}</h2>'''
            # -----------------------------------------------------------------

            if section.get('description'):
                html_content += f'\n        <p class="section-description">{section["description"]}</p>'

            videos_per_row = section['videos_per_row']
            for i in range(0, len(video_files), videos_per_row):
                row_uid_counter += 1
                row_id = f"video-row-other-{row_uid_counter}"
                
                # ****** 核心修改区域：移除 Demo Video 的播放按钮 ******
                if section['title'] != 'Demo Video':
                    # 如果不是 Demo Video，则生成播放按钮
                    html_content += f'\n        <button class="play-row-btn" onclick="playRow(\'{row_id}\')">▶ Play All Videos in Row</button>'
                # ****** 核心修改区域结束 ******

                html_content += f'\n        <div class="video-row" id="{row_id}">'
                row_videos = video_files[i:i + videos_per_row]
                for video_file in row_videos:
                    video_path = os.path.join(VIDEOS_ROOT_DIR, section['folder'], video_file)
                    video_path_url = video_path.replace(os.sep, "/")
                    
                    # 关键改动：如果是 Demo Video，用原始分辨率样式
                    if section['title'] == 'Demo Video':
                        html_content += create_video_element(video_path_url, section['folder'], annotations, video_ratio_class="video-original-size")
                    else:
                        html_content += create_video_element(video_path_url, section['folder'], annotations)
                html_content += '\n        </div>'
            html_content += '\n    </div>'

    html_content += '''
</body>
</html>'''
    return html_content

if __name__ == "__main__":
    print("Generating HTML page for supplementary videos...")
    annotations = {}
    if ANNOTATIONS_JSON_PATH and os.path.exists(ANNOTATIONS_JSON_PATH):
        try:
            with open(ANNOTATIONS_JSON_PATH, 'r', encoding='utf-8') as f:
                annotations = json.load(f)
            print(f"Successfully loaded annotations from '{ANNOTATIONS_JSON_PATH}'.")
        except json.JSONDecodeError:
            print(f"Warning: Could not decode JSON from '{ANNOTATIONS_JSON_PATH}'. Using filenames as descriptions.")
        except Exception as e:
            print(f"An error occurred while reading the annotation file: {e}")
    else:
        print(f"Warning: Annotation file '{ANNOTATIONS_JSON_PATH}' not found. Using filenames as descriptions.")

    if not os.path.isdir(VIDEOS_ROOT_DIR):
        print(f"Error: The directory '{VIDEOS_ROOT_DIR}' was not found.")
    else:
        final_html = generate_html(annotations)
        with open(OUTPUT_HTML_FILE, 'w', encoding='utf-8') as f:
            f.write(final_html)
        print(f"Successfully created '{OUTPUT_HTML_FILE}'.")
        try:
            webbrowser.open('file://' + os.path.realpath(OUTPUT_HTML_FILE))
            print("Opening the page in your default browser...")
        except Exception as e:
            print(f"Could not automatically open the file in a browser. Please open '{OUTPUT_HTML_FILE}' manually.")