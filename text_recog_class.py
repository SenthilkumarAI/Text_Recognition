import os
import sys
import cv2
import yaml
import json
import numpy as np
from rapidocr import RapidOCR
from Instantiate_Logger import Setup_Logger


class TextRecognizer(Setup_Logger):
    def __init__(self, image_path):
        super(TextRecognizer, self).__init__()
        self.image_path = image_path
        # self.logger = Setup_Logger()
        # self.logger.logger.info(f"Filename : {self.image_path}")
        self.logger.info(f"Filename : {self.image_path}\n")
        self.img = cv2.imread(self.image_path)
        self.gray_img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        self.binary_img = cv2.threshold(self.gray_img, 127, 255, cv2.THRESH_BINARY)[1]
        self.result = RapidOCR()(self.binary_img)
        self.write_to_json("image_data_class.json")


    def write_to_json(self, filename):
        try:
            assert self.result.txts and len(self.result.boxes) and self.result.scores, f"One of the elements from boxes, texts, scores are empty"
            try:
                assert len(self.result.boxes) == len(self.result.txts) == len(self.result.scores), f"lengths of boxes, texts, scores are different"
            except AssertionError as e:
                self.logger.error(f"Error Occured \n{e}",exc_info=True)
                sys.exit(1)

            self.box_txt_scr = []
            for box, txt, sco in zip(self.result.boxes, self.result.txts, self.result.scores):
                dict_fmt = dict()
                dict_fmt["bbox"] = {"tp_lft_crnr": box[0].astype(int).tolist(),
                                    "btm_rgt_crnr": box[2].astype(int).tolist()}
                dict_fmt["txt"] = txt
                dict_fmt['conf_score'] = sco
                self.box_txt_scr.append(dict_fmt)

            #  writing to Json file
            with open(filename, "w", encoding="utf-8") as json_file:
                json.dump(self.box_txt_scr, json_file, indent=5)
            self.logger.info(f"Writing to {os.path.join(os.getcwd(), filename)} completed")
        except AssertionError as e:
            self.logger.error(f"Error Occured \n{e}",exc_info=True)
            sys.exit(1)

    def draw_bb_on_image(self):
        for each in self.box_txt_scr:
            self.img_bbox = cv2.rectangle(self.img, tuple(each["bbox"]["tp_lft_crnr"]), tuple(each["bbox"]["btm_rgt_crnr"]),
                                (0, 255, 0), 1)
        img_bbox_fname = os.path.join(os.path.dirname(self.image_path), os.path.basename(self.image_path).split(".")[0] + "_with_bbox.png")
        cv2.imwrite(img_bbox_fname, self.img_bbox)
        self.logger.info(f"Drawing Bounding on {self.image_path} completed and saved to {img_bbox_fname}")

if __name__ == "__main__":
    tg = TextRecognizer("image2.png")
    tg.draw_bb_on_image()