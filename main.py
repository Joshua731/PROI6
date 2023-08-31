import sqlite3
import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Input, Output, State
from dash.exceptions import PreventUpdate
from flask import Flask, redirect, request, session
import jwt
import datetime
import functools
from flask import request, redirect

SECRET_KEY = "shua10!"

