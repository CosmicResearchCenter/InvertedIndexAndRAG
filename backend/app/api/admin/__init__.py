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
from app.core.utils.utils import get_is_admin

from app.core.services.admin.admin_service  import AdminService
from .admin import (ResponseGenral,
                    DeleteUserConversationRequest,
                    DeleteUserKnowledgeBaseRequest,
                    DeleteUserRequest,
                    GrantAdminRequest,
                    RevokeAdminRequest
                    )
router = APIRouter()

# 获取系统基本信息
@router.get("/system_info", response_model=ResponseGenral)
async def get_system_info(username: str = Depends(get_is_admin)):
    admin_service = AdminService()
    system_info = admin_service.get_system_info()
   
    return ResponseGenral(
        code=200,
        message="返回系统基本信息",
        data=[system_info]
    ) 

# 获取用户
@router.get("/users", response_model=ResponseGenral)
async def get_users_conversation(username: str = Depends(get_is_admin)):
    admin_service = AdminService()
    users = admin_service.get_all_users()
    return ResponseGenral(
        code=200,
        message="返回用户对话信息",
        data=[users]
    )

# 根据用户名获取对话列表
@router.get("/user_conversation/{username}", response_model=ResponseGenral)
async def get_user_conversation(username: str, s_username: str = Depends(get_is_admin)):
    admin_service = AdminService()
    user_conversation = admin_service.get_user_conversation(username,s_username)
    return ResponseGenral(
        code=200,
        message="返回用户对话信息",
        data=[user_conversation]
    )
# 根据对话id获取对话信息
@router.get("/conversation/{conversation_id}", response_model=ResponseGenral)
async def get_conversation(conversation_id: str, username: str = Depends(get_is_admin)):
    admin_service = AdminService()
    conversation = admin_service.get_conversation_content(conversation_id,username)
    return ResponseGenral(
        code=200,
        message="返回对话信息",
        data=[conversation]
    )

# 获取用户知识库信息
@router.get("/user_knowledge_base/{username}", response_model=ResponseGenral)
async def get_user_knowledge_base(username: str, s_username: str = Depends(get_is_admin)):
    admin_service = AdminService()
    user_knowledge_base = admin_service.get_user_knowledge_base(username,s_username)
    return ResponseGenral(
        code=200,
        message="返回用户知识库信息",
        data=[user_knowledge_base]
    )

    
# 删除用户
@router.delete("/delete_user", response_model=ResponseGenral)
async def delete_user(delete_user_request: DeleteUserRequest, username: str = Depends(get_is_admin)):
    admin_service = AdminService()
    admin_service.delete_user(delete_user_request.username)
    return ResponseGenral(
        code=200,
        message="删除用户成功",
        data=[]
    )
    
# 删除用户对话
@router.delete("/delete_user_conversation", response_model=ResponseGenral)
async def delete_user_conversation(delete_user_conversation_request: DeleteUserConversationRequest, username: str = Depends(get_is_admin)):
    admin_service = AdminService()
    admin_service.delete_user_conversation(delete_user_conversation_request.username,delete_user_conversation_request.conversation_id)
    return ResponseGenral(
        code=200,
        message="删除用户对话成功",
        data=[]
    )
    
# 删除用户知识库
@router.delete("/delete_user_knowledge_base", response_model=ResponseGenral)
async def delete_user_knowledge_base(delete_user_knowledge_base_request: DeleteUserKnowledgeBaseRequest,username: str = Depends(get_is_admin)):
    admin_service = AdminService()
    admin_service.delete_user_knowledge_base(delete_user_knowledge_base_request.username,delete_user_knowledge_base_request.knowledge_base_id)
    return ResponseGenral(
        code=200,
        message="删除用户知识库成功",
        data=[]
    )
    
# 授予用户管理员权限
@router.post("/grant_admin", response_model=ResponseGenral)
async def grant_admin(grant_admin_request: GrantAdminRequest,user: str = Depends(get_is_admin)):
    admin_service = AdminService()
    admin_service.grant_user_admin(grant_admin_request.username)
    return ResponseGenral(
        code=200,
        message="授予用户管理员权限成功",
        data=[]
    )
    
# 撤销用户管理员权限
@router.post("/revoke_admin", response_model=ResponseGenral)
async def revoke_admin(revoke_admin_request: RevokeAdminRequest,user: str = Depends(get_is_admin)):
    admin_service = AdminService()
    admin_service.revoke_user_admin(revoke_admin_request.username)
    return ResponseGenral(
        code=200,
        message="撤销用户管理员权限成功",
        data=[]
    )


