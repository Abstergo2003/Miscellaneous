package com.abstergo2003.http;

public class HttpRequest extends HttpMessage{
    private HttpMethod method;
    private String requestTarget;
    private String originalHttpVersion;
    private HttpVersion bestCompatibleVersion;
    private String Body;
    private String Connection;
    public HttpMethod getMethod() {
        return method;
    }

    void setMethod(String methodName) throws HttpParsingException {
        for (HttpMethod method: HttpMethod.values()) {
            if (methodName.equals(method.name())) {
                this.method = method;
                return;
            }
        }
        throw new HttpParsingException(HttpStatusCode.SERVER_ERROR_501_NOT_IMPLEMENTED);
    }

    public String getTarget() {
        return this.requestTarget;
    }

    public void setTarget(String requestTarget) throws HttpParsingException {
        if (requestTarget == null || requestTarget.isEmpty()) {
            throw new HttpParsingException(HttpStatusCode.SERVER_ERROR_500_INTERNAL_SERVER_ERROR);
        }
        this.requestTarget = requestTarget;
    }


    public HttpVersion getHttpVersion() {
        return this.bestCompatibleVersion;
    }

    void setHttpVersion(String originalHttpVersion) throws BadHTTPVersionException, HttpParsingException {
        this.originalHttpVersion = originalHttpVersion;
        this.bestCompatibleVersion = HttpVersion.getBestCompatibleVersion(originalHttpVersion);
        if (this.bestCompatibleVersion == null) {
            throw new HttpParsingException(HttpStatusCode.SERVER_ERROR_505_HTTP_VERSION_NOT_SUPPORTED);
        }
    }

    public String getBody() {
        return this.Body;
    }

    public void setBody(String body) {
        this.Body = body;
    }

    public String getConnection() {
        return this.Connection;
    }

    public void setConnection(String connection) {
        this.Connection = connection;
    }
    public String getArgument(String argName) {
        String[] args = this.requestTarget.split("&");
        for (String arg: args) {
            if (arg.contains(argName)) {
                String[] split = arg.split("=", 2);
                return split[1];
            }
        }
        return "";
    }
}
