package com.abstergo2003.http;

import org.junit.Test;

import static org.junit.Assert.*;

public class HttpVersionTest {
    @Test
    public void getBestCompatibleVersionExactMatch() {
        HttpVersion version = null;
        try {
            version = HttpVersion.getBestCompatibleVersion("HTTP/1.1");
        } catch (BadHTTPVersionException e) {;
           fail();
        }

        assertNotNull(version);
        assertEquals(version, HttpVersion.HTTP_1_1);
    }

    @Test
    public void getBestCompatibleVersionBadFormat() {
        HttpVersion version = null;
        try {
            version = HttpVersion.getBestCompatibleVersion("httP/1.1");
            fail();
        } catch (BadHTTPVersionException e) {;

        }
    }

    @Test
    public void getBestCompatibleVersionHigherVersion() {
        HttpVersion version = null;
        try {
            version = HttpVersion.getBestCompatibleVersion("HTTP/1.2");
            assertNotNull(version);
            assertEquals(version, HttpVersion.HTTP_1_1);
        } catch (BadHTTPVersionException e) {;
            fail();
        }
    }
}