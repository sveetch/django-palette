## -*- coding: utf-8 -*-
#import os
#import json

#from pathlib import Path

#import pytest

#import click
#from click.testing import CliRunner

#from sveetoy_cli.cli.console_script import cli_frontend


#def test_empty(caplog, testsettings):
    #"""Invoked without required arguments"""
    #runner = CliRunner()

    #with runner.isolated_filesystem():
        #test_cwd = os.getcwd()

        #result = runner.invoke(cli_frontend, ['colors'])

        #assert caplog.record_tuples == []

        #assert 'Error: Missing argument "source".' in result.output

        #assert result.exit_code == 2


#def test_doesnotexists(caplog, testsettings):
    #"""Invoked without required arguments"""
    #runner = CliRunner()

    #with runner.isolated_filesystem():
        #test_cwd = os.getcwd()

        #result = runner.invoke(cli_frontend, ['colors'] + ['foo.txt'])

        #assert caplog.record_tuples == []

        #assert 'Invalid value for "source": Path "foo.txt" does not exist.' in result.output
        #assert result.exit_code == 2


#def test_source_as_file(caplog, testsettings):
    #"""Invoked with a file path as source argument"""
    #runner = CliRunner()

    #source_path = 'foo.txt'

    #with runner.isolated_filesystem():
        #test_cwd = os.getcwd()

        #source_file = Path(test_cwd) / source_path
        #source_file.write_text('Dummy')

        #result = runner.invoke(cli_frontend, ['colors'] + [source_path])

        #assert result.exit_code == 0

        #assert caplog.record_tuples == [
            #(
                #'sveetoy',
                #20,
                #"Search files for colors"
            #),
            #(
                #'sveetoy',
                #30,
                #"Unable to find any color from source(s)"
            #),
        #]


#def test_source_as_directory(caplog, testsettings):
    #"""Invoked with a directory path as source argument"""
    #runner = CliRunner()

    #source_path = 'bar'

    #with runner.isolated_filesystem():
        #test_cwd = os.getcwd()

        #source_dir = Path(test_cwd) / source_path
        #source_dir.mkdir(parents=True)

        #result = runner.invoke(cli_frontend, ['colors'] + [source_path])

        #assert result.exit_code == 0

        #assert caplog.record_tuples == [
            #(
                #'sveetoy',
                #20,
                #"Search files for colors"
            #),
            #(
                #'sveetoy',
                #30,
                #"Unable to find any color from source(s)"
            #),
        #]


#def test_sample1_as_file(caplog, testsettings):
    #"""
    #Searching color in sample-1 and write results to a JSON file
    #"""
    #basedir = testsettings.colors_path

    #fixture_filename = "sample-1.scss"
    #fixture_filepath = Path(basedir) / fixture_filename

    #runner = CliRunner()

    #with runner.isolated_filesystem():
        #args = [
            #'colors',
            #str(fixture_filepath),
            #"--to",
            #"plouf.json",
        #]
        #result = runner.invoke(cli_frontend, args, catch_exceptions=False)

        #print(result.output)

        #assert result.exit_code == 0

        #assert caplog.record_tuples == [
            #(
                #'sveetoy',
                #20,
                #"Search files for colors"
            #),
        #]


#def test_all_fixtures(caplog, testsettings):
    #"""
    #Searching color in every fixtures files and returning results as JSON
    #string in output
    #"""
    #basedir = testsettings.colors_path

    #runner = CliRunner()

    #result = runner.invoke(cli_frontend, ['--verbose', '0', 'colors'] + [basedir], catch_exceptions=False)

    #print(result.output)

    #assert result.exit_code == 0

    #assert caplog.record_tuples == []

    #assert json.loads(result.output) == json.loads("""{
    #"#fafafa": [
        #"gray98",
        #"#fafafa"
    #],
    #"#8461a1": [
        #"plum4",
        #"#8b668b"
    #],
    #"#ff8702": [
        #"darkorange",
        #"#ff8c00"
    #],
    #"#1a2955": [
        #"midnightblue",
        #"#191970"
    #],
    #"#4c4c92": [
        #"darkslateblue",
        #"#483d8b"
    #],
    #"#253a79": [
        #"royalblue4",
        #"#27408b"
    #],
    #"#b29e6b": [
        #"darkkhaki",
        #"#bdb76b"
    #],
    #"#222": [
        #"gray13",
        #"#212121"
    #],
    #"#6676a2": [
        #"slategray4",
        #"#6c7b8b"
    #],
    #"#00ff00": [
        #"green1",
        #"#00ff00"
    #]
#}""")
