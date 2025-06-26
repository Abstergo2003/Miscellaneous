package com.abstergo2003.http;

import java.io.IOException;
import java.io.OutputStream;

public class HttpResponse {
    private final HttpStatusCode statusCode;
    private final byte[] body;
    private final String contentType;
    private final HttpVersion version;

    public HttpResponse(HttpStatusCode statusCode, byte[] body, String contentType, HttpVersion version) {
        this.statusCode = statusCode;
        this.body = body;
        this.contentType = contentType;
        this.version = version;
    }

    public void send(OutputStream outputStream) throws IOException {
        String statusLine = version.LITERAl + " " + statusCode.STATUS_CODE + " " + statusCode.MESSAGE + "\r\n";
        String contentTypeHeader = "Content-Type: " + contentType + "\r\n";
        String contentLengthHeader = "Content-Length: " + body.length + "\r\n\r\n";

        outputStream.write(statusLine.getBytes());
        outputStream.write(contentTypeHeader.getBytes());
        outputStream.write(contentLengthHeader.getBytes());
        outputStream.write(body);
        outputStream.flush();
    }
}
