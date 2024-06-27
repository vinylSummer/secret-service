CREATE TABLE memes (
    id BIGSERIAL PRIMARY KEY,
    unique_meme_id VARCHAR UNIQUE NOT NULL,
    unique_image_id VARCHAR UNIQUE NOT NULL,
    caption VARCHAR
);

CREATE INDEX ON memes(unique_meme_id);
CREATE INDEX ON memes(unique_image_id);
