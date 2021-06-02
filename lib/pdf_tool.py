from pathlib import Path

import os
import fitz


def pdf2png(file_path, output_dir, password=None):
    list = []
    doc = fitz.open(file_path)
    
    if doc.needs_pass:
        doc.authenticate(password)
    
    for page in doc:
        pix = page.get_pixmap()
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        result_path = os.path.join(
            output_dir, f"{page.number}.png")
        pix.save(result_path)
        list.append(result_path)

    return list


def draw_rects(file_path, page_rects, output_dir, password=None):
    doc = fitz.open(file_path)

    if doc.needs_pass:
        doc.authenticate(password)

    for page_rect in page_rects:
        page = doc[page_rect['page']-1]
        shape = page.new_shape()
        for rect in page_rect['rects']:
            shape.draw_rect(
                fitz.Rect(rect[0], rect[1], rect[0]+rect[2], rect[1]+rect[3]))
            shape.finish(width=0.3, color=(1, 0, 0))
            shape.commit()
    
    full_filename = os.path.split(file_path)[1]
    diff_filename = os.path.splitext(full_filename)[0] + '-diff' + os.path.splitext(full_filename)[1]
    diff_file_path = os.path.join(output_dir, diff_filename) 
    doc.save(diff_file_path)
    
    return diff_filename
