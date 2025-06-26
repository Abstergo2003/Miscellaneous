package com.abstergo2003.http;

public enum HttpMethod {
    GET, HEAD, POST;

    public static final int MAX_LENGTH;

    HttpMethod() {
    }
    static {
        int tempMax = -1;
        for (HttpMethod method: values()) {
            if (method.name().length() > tempMax) {
                tempMax = method.name().length();
            }
        }
        MAX_LENGTH = tempMax;
    }
}
