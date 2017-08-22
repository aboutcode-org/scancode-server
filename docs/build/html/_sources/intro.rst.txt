Introduction
===========================================

This is a server for the ScanCode toolkit(https://github.com/nexB/scancode-toolkit).

A project which uses ScanCode as a library in a web and REST API application that allows you to scan code on demand by entering a URL and then store the scan results.

This is a work-in-progress...

The goal is to provide a minimal web UI and a comprehensive REST API to:

 - scan code for origin, licensing and dependencies for a remote URL, a
   remote repo or a file upload.
 - store scan results and eventually offer a central storage place for
   ScanCode scans even when done using the ScanCode CLI app.
 - offer some Travis and/or Github integration to scan on commit with
   webhooks.
 - eventually offer extra goodies such as scan based on a received tweet
   of similar IRC or IM integration.