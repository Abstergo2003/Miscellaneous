package com.abstergo2003.http;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

public enum HttpVersion {
    HTTP_1_1("HTTP/1.1", 1, 1);

    public final String LITERAl;
    public final int MAJOR;
    public final int MINOR;

    HttpVersion(String literal, int major, int minor) {
        this.LITERAl = literal;
        this.MAJOR = major;
        this.MINOR = minor;
    }
    private static final Pattern httpVersionRegexPattern = Pattern.compile("^HTTP/(?<major>\\d+).(?<minor>\\d+)");
    public static HttpVersion getBestCompatibleVersion(String literalVersion) throws BadHTTPVersionException {
        Matcher matcher = httpVersionRegexPattern.matcher(literalVersion);
        if (!matcher.find() || matcher.groupCount() != 2) {
            throw new BadHTTPVersionException();
        }
        int major = Integer.parseInt(matcher.group("major"));
        int minor = Integer.parseInt(matcher.group("minor"));

        HttpVersion tempBest = null;
        for (HttpVersion version: HttpVersion.values()) {
            if (version.LITERAl.equals(literalVersion)) {
                return version;
            } else {
                if (version.MAJOR == major) {
                    if (version.MINOR < minor) {
                        tempBest = version;
                    }
                }
            }
        }
        return tempBest;
    }
}
