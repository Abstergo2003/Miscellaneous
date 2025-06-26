package com.abstergo2003.testserver.config;

public class HttpConfigurationExcpetion extends RuntimeException{
    public HttpConfigurationExcpetion() {
    }

    public HttpConfigurationExcpetion(String message) {
        super(message);
    }

    public HttpConfigurationExcpetion(String message, Throwable cause) {
        super(message, cause);
    }

    public HttpConfigurationExcpetion(Throwable cause) {
        super(cause);
    }
}
