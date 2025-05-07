from config import Config
from logger import Logger
from poster import Poster


class App:
    def run(self):
        """Run app: load config, start session, and post to groups."""
        logger = Logger()
        logger.info("Starting...")

        cfg = Config(logger=logger)
        poster = Poster(
            cookie=cfg.get("cookie"),
            img_path=cfg.get("image"),
            text=cfg.get("text"),
            logger=logger,
        )

        grps_ids = cfg.get("groups")
        poster.start_session()

        for grp_id in grps_ids:
            poster.post(grp_id=grp_id)
            logger.info(f"Posted to group: {grp_id}")

        poster.stop_session()
        logger.info("Done.")
