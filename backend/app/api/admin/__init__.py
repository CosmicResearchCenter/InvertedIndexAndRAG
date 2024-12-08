"""
后台管理员部分的路由
"""
from fastapi import APIRouter, Depends, HTTPException, status
import hashlib
import jwt
import datetime
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from config.config_info import settings
from app.core.database.mysql_client import MysqlClient
from app.core.database.models import UserInfo
from app.core.utils.utils import get_current_user

from app.core.services.admin.admin_service  import AdminService
from .admin import ResponseGenral
router = APIRouter()

# 获取系统基本信息
@router.get("/system_info", response_model=ResponseGenral)
async def get_system_info():
    admin_service = AdminService()
    system_info = admin_service.get_system_info()
   
    return ResponseGenral(
        code=200,
        message="返回系统基本信息",
        data=[system_info]
    ) 

# 获取用户对话信息
@router.get("/users_conversation", response_model=ResponseGenral)
async def get_users_conversation():
    admin_service = AdminService()
    user_conversation = admin_service.get_users_conversation()
    return ResponseGenral(
        code=200,
        message="返回用户对话信息",
        data=[user_conversation]
    )
    
# 获取用户知识库信息
@router.get("/users_knowledge_base", response_model=ResponseGenral)
async def get_users_knowledge_base():
    admin_service = AdminService()
    user_knowledge_base = admin_service.get_users_knowledge_base()
    return ResponseGenral(
        code=200,
        message="返回用户知识库信息",
        data=[user_knowledge_base]
    )

