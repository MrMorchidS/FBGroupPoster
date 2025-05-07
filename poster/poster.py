from .base_poster import BasePoster
import os


class Poster(BasePoster):
    def __init__(self, cookie: str, img_path: str, text: str, logger) -> None:
        super().__init__(
            cookie=cookie, url="https://mbasic.facebook.com", logger=logger
        )
        self._img_path = img_path
        self._text = text

    # ------------------------------
    # Session Setup
    # ------------------------------
    def start_session(self) -> None:
        """Start session"""
        if not self._cookie:
            self._logger.error("Authentication cookie missing. Exiting application.")
            os._exit(1)

        if not self._img_path:
            super()._start_rq_session()
        else:
            if not os.path.exists(self._img_path):
                self._logger.error(f"Image file not found: {self._img_path}. Exiting.")
                os._exit(1)
            super()._start_pw_session()

    def stop_session(self) -> None:
        """Stop session"""
        if not self._img_path:
            super()._stop_rq_session()
        else:
            super()._stop_pw_session()

    # ------------------------------
    # Posting Methods
    # ------------------------------
    def post(self, grp_id: str) -> None:
        """Post text or image to Facebook groups via mbasic."""
        if not self._img_path:
            self._post_text(grp_id=grp_id)
        else:
            self._post_text_with_image(grp_id=grp_id)

    def _post_text(self, grp_id: str) -> None:
        """Post text to group."""
        soup = self._get_soup(f"{self._url}/groups/{grp_id}")
        if not soup:
            return

        form = soup.find("form", method="post")
        if not form:
            return

        action_url = form.get("action")
        if not action_url:
            return

        data = {}
        for tag in form.find_all("input"):
            name = tag.get("name")
            if not name:
                continue
            data[name] = tag.get("value", "")

        data.update({"xc_message": self._text, "view_post": "Posting"})
        self._session.post(f"{self._url}/{action_url}", data=data)

    def _post_text_with_image(self, grp_id: str) -> None:
        """Post text with image to group."""
        self._goto_url(f"{self._url}/groups/{grp_id}")
        if not self._is_visible("input[name='view_photo']"):
            return

        self._click_btn(("input[name='view_photo']"))

        if self._is_visible("form div.z div.ba input[name='file1']"):
            self._upload_img(
                sel="form div.z div.ba input[name='file1']", path=self._img_path
            )
        elif self._is_visible(
            "#root > table > tbody > tr > td > form > div.ba > div > input:nth-child(1)"
        ):
            self._upload_img(
                sel="#root > table > tbody > tr > td > form > div.ba > div > input:nth-child(1)",
                path=self._img_path,
            )
        else:
            return

        if self._is_visible("form div.ba input[name='add_photo_done']"):
            self._click_btn("form div.ba input[name='add_photo_done']")
        elif self._is_visible(
            "#root > table > tbody > tr > td > form > div.bb > input.bh.bi.bj.bk.bl"
        ):
            self._click_btn(
                "#root > table > tbody > tr > td > form > div.bb > input.bh.bi.bj.bk.bl"
            )
        else:
            return

        if not self._is_visible("textarea"):
            return
        self._fill_input(selctor="textarea", value=self._text)

        if not self._is_visible("form input[name='view_post']"):
            return
        self._click_btn("form input[name='view_post']")

    def _upload_img(self, sel: str, path: str) -> None:
        """Upload image using selector."""
        self._page.wait_for_selector(sel)
        self._page.locator(sel).set_input_files(path)
