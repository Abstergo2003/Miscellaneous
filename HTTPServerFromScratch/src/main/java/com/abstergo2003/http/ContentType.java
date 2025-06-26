package com.abstergo2003.http;

public enum ContentType {
    TEXT_PLAIN("text/plain", ".txt"),
    TEXT_HTML("text/html", ".html"),
    TEXT_CSS("text/css", ".css"),
    TEXT_JAVASCRIPT("text/javascript", ".js"),
    TEXT_XML("text/xml", ".xml"),

    IMAGE_JPEG("image/jpeg", ".jpeg"),
    IMAGE_JPG("image/jpeg", ".jpg"),
    IMAGE_PNG("image/png", ".png"),
    IMAGE_GIF("image/gif", ".gif"),
    IMAGE_BMP("image/bmp", ".bmp"),
    IMAGE_SVG("image/svg+xml", ".svg"),
    IMAGE_ICON("image/x-icon", ".ico"),

    AUDIO_MPEG("audio/mpeg", ".mp3"),
    AUDIO_wav("audio/wav", ".wav"),
    AUDIO_OGG("audio/ogg", ".ogg"),

    VIDEO_MP4("video/mp4", ".mp4"),
    VIDEO_MPEG("video/mpeg", ".mpeg"),
    VIDEO_WEBM("video/webm", ".webm"),

    APPLICATION_JSON("application/json", ".json"),
    APPLICATION_XML("application/xml", ".xml"),
    APPLICATION_PDF("application/pdf", ".pdf"),
    APPLICATION_WORD("application/msword", ".doc"),
    APPLICATION_EXCEL("application/vnd.ms-excel", ".xls"),

    ;

    private final String message;
    private final String extension;
    ContentType(String message, String extension) {
        this.message = message;
        this.extension = extension;
    };

    public static ContentType matchContentType(String filePath) {
        int index = filePath.lastIndexOf(".");
        String extension = filePath.substring(index);
        for (ContentType type: ContentType.values()) {
            if (type.extension.equals(extension)) {
                return type;
            }
        }
        return ContentType.TEXT_PLAIN;
    }

    public String getMessage() {
        return this.message;
    }
}
