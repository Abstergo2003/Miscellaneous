package com.abstergo2003.http;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class HttpParser {
    private final static Logger LOGGER = LoggerFactory.getLogger(HttpParser.class);

    private static final int SP = 0x20; //32
    private static final int CR = 0x0D; //13
    private static final int LF = 0x0A; //10



    public static HttpRequest parseHttpRequest(InputStream inputStream) throws HttpParsingException, IOException, BadHTTPVersionException {
        InputStreamReader reader = new InputStreamReader(inputStream, StandardCharsets.US_ASCII);

        BufferedReader stringReader = new BufferedReader(reader);
        StringBuilder requestBuilder = new StringBuilder();
        String line;
        while ((line = stringReader.readLine()) != null && !line.isEmpty()) {
            requestBuilder.append(line).append("\r\n");
        }
        String stringRequest = requestBuilder.toString();

        HttpRequest request = new HttpRequest();

        parseRequestLine(stringRequest, request);
        parseHeaders(stringRequest, request);
        parseBody(stringRequest, request);


        LOGGER.info("Request Method: " + request.getMethod());
        LOGGER.info("Request Target: " + request.getTarget());
        LOGGER.info("Request HTTP Version: " + request.getHttpVersion());
        LOGGER.info("Request Connection Type: " + request.getConnection());
        LOGGER.info("Request Body: " + request.getBody());
        return request;
    }

    private static void parseBody(String stringRequest, HttpRequest request) throws IOException {

        String[] parts = stringRequest.split("\r\n\r\n", 2);
        if (parts.length > 1) {
            request.setBody(parts[1]);
        } else {
            request.setBody("");
        }
    }

    private static void parseHeaders(String stringRequest, HttpRequest request) throws IOException {

        String pattern = "Connection" + ":\\s*([^\r\n]+)";
        Pattern regex = Pattern.compile(pattern);
        Matcher matcher = regex.matcher(stringRequest);

        if (matcher.find()) {
            String connection =  matcher.group(1);
            request.setConnection(connection);
        }
    }

    private static void parseRequestLine(String stringRequest, HttpRequest request) throws HttpParsingException, BadHTTPVersionException {
        String line = stringRequest.split("\r\n")[0];
        String[] parts = line.split(" ");
        if (parts.length != 3) {
            throw new HttpParsingException(HttpStatusCode.CLIENT_ERROR_400_BAD_REQUEST);
        }
        request.setMethod(parts[0]);
        request.setTarget(parts[1].replaceAll("%20", " "));
        request.setHttpVersion(parts[2]);
    }
}

