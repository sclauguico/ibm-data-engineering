ALTER TABLE BookShop
ADD CONSTRAINT fk_BookShop FOREIGN KEY (AUTHOR_ID)
    REFERENCES BookShop_AuthorDetails(AUTHOR_ID)
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;