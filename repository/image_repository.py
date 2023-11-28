from models.product_model import Image
from sqlalchemy.orm import Session


class ImageRepository:

    @staticmethod
    async def create_image(db: Session, filename, product_id):
        new_image = Image(filename=filename, product_id=product_id)
        db.add(new_image)
        db.commit()
        db.refresh(new_image)
        return new_image

    @staticmethod
    async def get_image_by_product_id(db: Session, product_id):
        image = db.query(Image).filter_by(product_id=product_id).first()
        return image
