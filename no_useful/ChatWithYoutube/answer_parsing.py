import re

def parse_answer(text, video_id):
    bracket_contents = re.findall(r'\[[^\]]+\]', text)
    vid_content = ''
    for content in bracket_contents:
        numbers = re.findall(r'\d+\.\d+', content)
        if numbers:
            replacement_text = "".join([
                f'<a style="text-decoration: none;" href="https://www.youtube.com/embed/{video_id}?start={int(float(number))}&autoplay=1&mute=1" target="youtube_vid{number}" id="{number}"><sup>[{number}]</sup></a>'
                for number in numbers
            ])
            vid_content += "".join([f'<div><iframe width="100%" name="youtube_vid{number}" frameborder="0"></iframe></div>' for number in numbers])
            text = text.replace(f'{content}', f'{replacement_text}')
    return text, vid_content
