package com.abstergo2003.testserver.core;

import com.abstergo2003.http.*;
import com.abstergo2003.testserver.util.FileHandler;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.Socket;

public class HttpConnectionWorkerThread extends Thread{
    private Socket socket;
    private final static Logger LOGGER = LoggerFactory.getLogger(HttpConnectionWorkerThread.class);
    public HttpConnectionWorkerThread(Socket socket){
        this.socket = socket;
    }
    @Override
    public void run() {

        InputStream inputStream = null;
        OutputStream outputStream = null;
        try {
            inputStream = socket.getInputStream();
            outputStream = socket.getOutputStream();

            HttpRequest request = HttpParser.parseHttpRequest(inputStream);
            if (request.getMethod() == HttpMethod.GET) {
                String target = request.getTarget();
                ContentType type = FileHandler.getContentType(target);
                String filePath = FileHandler.parsePath(target);
                HttpResponse response = new HttpResponse(HttpStatusCode.SUCCESS_200_OK, FileHandler.readFile(filePath), type.getMessage(), request.getHttpVersion());
                response.send(outputStream);
            } else if (request.getMethod() == HttpMethod.POST) {
                ContentType type = ContentType.APPLICATION_JSON;
                String bodyResponse = ApiFunctions.parseFunction(request);
                HttpResponse response = new HttpResponse(HttpStatusCode.SUCCESS_200_OK, bodyResponse.getBytes(), type.getMessage(), request.getHttpVersion());
                response.send(outputStream);
            }
            LOGGER.info("Connection handled");
        } catch (IOException e) {
            LOGGER.error("Problem with communication", e);
            HttpResponse response = new HttpResponse(HttpStatusCode.CLIENT_ERROR_404_NOT_FOUND, "".getBytes(), ContentType.TEXT_PLAIN.getMessage(), HttpVersion.HTTP_1_1);
            try {
                assert outputStream != null;
                response.send(outputStream);
            } catch (IOException ex) {
                throw new RuntimeException(ex);
            }
        } catch (HttpParsingException | BadHTTPVersionException e) {
            throw new RuntimeException(e);
        } finally {
            if (inputStream != null) {
                try {
                    inputStream.close();
                } catch (IOException e) {}
            }
            if (outputStream != null) {
                try {
                    outputStream.close();
                } catch (IOException e) {}
            }
            if (socket != null) {
                try {
                    LOGGER.info("Socket Closed");
                    socket.close();
                } catch (IOException e) {}
            }
        }
    }
}
