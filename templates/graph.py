from flask import Flask,session, request,render_template
import db
import cx_Oracle
import os
import sys
#연결에 필요한 기본 정보 (유저, 비밀번호, 데이터베이스 서버 주소)

whaday="2022.10.08"
