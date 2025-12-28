from sqlalchemy.orm import Session
from app.models.task import Task
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Any
from io import BytesIO

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

def get_tasks_analytics(db: Session) -> Dict[str, Any]:
    tasks = db.query(Task).all()
    
    if not tasks:
        return {
            "total_tasks": 0,
            "by_status": {},
            "by_priority": {},
            "by_assignee": {},
            "status_percentage": {},
            "priority_percentage": {}
        }
    
    df = pd.DataFrame([{
        "id": task.id,
        "status": task.status,
        "priority": task.priority,
        "assignee": task.assignee,
        "created_at": task.created_at
    } for task in tasks])
    
    total = len(df)
    
    by_status = df.groupby("status").size().to_dict()
    by_priority = df.groupby("priority").size().to_dict()
    by_assignee = df.groupby("assignee").size().to_dict() if not df["assignee"].isna().all() else {}
    
    status_percentage = {k: round((v / total) * 100, 2) for k, v in by_status.items()}
    priority_percentage = {k: round((v / total) * 100, 2) for k, v in by_priority.items()}
    
    return {
        "total_tasks": total,
        "by_status": by_status,
        "by_priority": by_priority,
        "by_assignee": by_assignee,
        "status_percentage": status_percentage,
        "priority_percentage": priority_percentage
    }

def generate_tasks_chart(db: Session) -> BytesIO:
    tasks = db.query(Task).all()
    
    if not tasks:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.text(0.5, 0.5, 'No tasks available', ha='center', va='center', fontsize=16)
        ax.set_xticks([])
        ax.set_yticks([])
        buf = BytesIO()
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        plt.close()
        buf.seek(0)
        return buf
    
    df = pd.DataFrame([{
        "status": task.status,
        "priority": task.priority,
        "assignee": task.assignee,
    } for task in tasks])
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Tasks Analytics Dashboard', fontsize=16, fontweight='bold')
    
    status_counts = df['status'].value_counts()
    axes[0, 0].bar(status_counts.index, status_counts.values, color='#3498db')
    axes[0, 0].set_title('Tasks by Status')
    axes[0, 0].set_xlabel('Status')
    axes[0, 0].set_ylabel('Count')
    axes[0, 0].tick_params(axis='x', rotation=45)
    
    priority_counts = df['priority'].value_counts()
    axes[0, 1].bar(priority_counts.index, priority_counts.values, color='#e74c3c')
    axes[0, 1].set_title('Tasks by Priority')
    axes[0, 1].set_xlabel('Priority')
    axes[0, 1].set_ylabel('Count')
    
    if not df['assignee'].isna().all() and len(df['assignee'].dropna()) > 0:
        assignee_counts = df['assignee'].value_counts().head(10)
        axes[1, 0].barh(assignee_counts.index, assignee_counts.values, color='#2ecc71')
        axes[1, 0].set_title('Tasks by Assignee (Top 10)')
        axes[1, 0].set_xlabel('Count')
        axes[1, 0].set_ylabel('Assignee')
    else:
        axes[1, 0].text(0.5, 0.5, 'No assignees', ha='center', va='center')
        axes[1, 0].set_title('Tasks by Assignee')
    
    status_pct = (df['status'].value_counts(normalize=True) * 100).round(2)
    axes[1, 1].pie(status_pct.values, labels=status_pct.index, autopct='%1.1f%%', startangle=90)
    axes[1, 1].set_title('Status Distribution (%)')
    
    plt.tight_layout()
    
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    plt.close()
    buf.seek(0)
    return buf