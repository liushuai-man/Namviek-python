// Runtime shim replacing @prisma/client enums for the Python backend migration.
// Provides actual JavaScript values (not just TypeScript types).
// This file is loaded at runtime via webpack alias configured in next.config.js.

const TaskPriority = Object.freeze({
  NONE: 'NONE',
  LOW: 'LOW',
  MEDIUM: 'MEDIUM',
  NORMAL: 'NORMAL',
  HIGH: 'HIGH',
  URGENT: 'URGENT'
})

const StatusType = Object.freeze({
  TODO: 'TODO',
  IN_PROGRESS: 'IN_PROGRESS',
  INPROCESS: 'INPROCESS',
  DONE: 'DONE'
})

const TaskType = Object.freeze({
  TASK: 'TASK',
  SUBTASK: 'SUBTASK',
  BUG: 'BUG',
  STORY: 'STORY',
  NEW_FEATURE: 'NEW_FEATURE',
  IMPROVEMENT: 'IMPROVEMENT'
})

const MemberRole = Object.freeze({
  ADMIN: 'ADMIN',
  MEMBER: 'MEMBER',
  GUEST: 'GUEST',
  MANAGER: 'MANAGER',
  LEADER: 'LEADER'
})

const UserStatus = Object.freeze({
  ACTIVE: 'ACTIVE',
  INACTIVE: 'INACTIVE',
  PENDING: 'PENDING'
})

const OrgStorageType = Object.freeze({
  LOCAL: 'LOCAL',
  S3: 'S3',
  MINIO: 'MINIO',
  AWS_S3: 'AWS_S3',
  DIGITAL_OCEAN_S3: 'DIGITAL_OCEAN_S3'
})

const FieldType = Object.freeze({
  TEXT: 'TEXT',
  NUMBER: 'NUMBER',
  DATE: 'DATE',
  PERSON: 'PERSON',
  SELECT: 'SELECT',
  MULTISELECT: 'MULTISELECT',
  CHECKBOX: 'CHECKBOX',
  FILES: 'FILES',
  URL: 'URL',
  EMAIL: 'EMAIL',
  CREATED_BY: 'CREATED_BY',
  CREATED_AT: 'CREATED_AT',
  UPDATED_BY: 'UPDATED_BY',
  UPDATED_AT: 'UPDATED_AT'
})

const FileType = Object.freeze({
  IMAGE: 'IMAGE',
  DOCUMENT: 'DOCUMENT',
  VIDEO: 'VIDEO',
  AUDIO: 'AUDIO',
  FILE: 'FILE',
  OTHER: 'OTHER'
})

const FileOwnerType = Object.freeze({
  TASK: 'TASK',
  PROJECT: 'PROJECT',
  USER: 'USER',
  ORGANIZATION: 'ORGANIZATION'
})

const ActivityType = Object.freeze({
  CREATE: 'CREATE',
  UPDATE: 'UPDATE',
  DELETE: 'DELETE',
  COMMENT: 'COMMENT',
  ASSIGN: 'ASSIGN',
  STATUS_CHANGE: 'STATUS_CHANGE',
  PRIORITY_CHANGE: 'PRIORITY_CHANGE',
  TASK_CREATED: 'TASK_CREATED',
  TASK_TITLE_CHANGED: 'TASK_TITLE_CHANGED',
  TASK_DESC_CHANGED: 'TASK_DESC_CHANGED',
  TASK_DUEDATE_CHANGED: 'TASK_DUEDATE_CHANGED',
  TASK_ASSIGNEE_ADDED: 'TASK_ASSIGNEE_ADDED',
  TASK_ASSIGNEE_REMOVED: 'TASK_ASSIGNEE_REMOVED',
  TASK_STATUS_CHANGED: 'TASK_STATUS_CHANGED',
  TASK_PRIORITY_CHANGED: 'TASK_PRIORITY_CHANGED',
  TASK_POINT_CHANGED: 'TASK_POINT_CHANGED',
  TASK_PROGRESS_CHANGED: 'TASK_PROGRESS_CHANGED',
  TASK_VISION_CHANGED: 'TASK_VISION_CHANGED',
  TASK_COMMENT_CREATED: 'TASK_COMMENT_CREATED',
  TASK_COMMENT_CHANGED: 'TASK_COMMENT_CHANGED',
  TASK_COMMENT_REMOVED: 'TASK_COMMENT_REMOVED',
  TASK_ATTACHMENT_ADDED: 'TASK_ATTACHMENT_ADDED',
  TASK_ATTACHMENT_REMOVED: 'TASK_ATTACHMENT_REMOVED'
})

const ActivityObjectType = Object.freeze({
  TASK: 'TASK',
  PROJECT: 'PROJECT',
  COMMENT: 'COMMENT',
  CHECKLIST: 'CHECKLIST'
})

const DashboardComponentType = Object.freeze({
  CHART: 'CHART',
  TABLE: 'TABLE',
  STAT: 'STAT',
  CUSTOM: 'CUSTOM',
  SUMMARY: 'SUMMARY',
  COLUMN: 'COLUMN',
  PIE: 'PIE',
  BURNDOWN: 'BURNDOWN',
  BURNUP: 'BURNUP'
})

const ProjectViewType = Object.freeze({
  LIST: 'LIST',
  BOARD: 'BOARD',
  CALENDAR: 'CALENDAR',
  GANTT: 'GANTT',
  GRID: 'GRID',
  GOAL: 'GOAL',
  TEAM: 'TEAM',
  ACTIVITY: 'ACTIVITY',
  DASHBOARD: 'DASHBOARD',
  TIMELINE: 'TIMELINE'
})

const InvitationStatus = Object.freeze({
  PENDING: 'PENDING',
  ACCEPTED: 'ACCEPTED',
  REJECTED: 'REJECTED'
})

const OrganizationRole = Object.freeze({
  OWNER: 'OWNER',
  ADMIN: 'ADMIN',
  MEMBER: 'MEMBER'
})

const Prisma = Object.freeze({
  Json: {}
})

module.exports = {
  TaskPriority,
  StatusType,
  TaskType,
  MemberRole,
  UserStatus,
  OrgStorageType,
  FieldType,
  FileType,
  FileOwnerType,
  ActivityType,
  ActivityObjectType,
  DashboardComponentType,
  ProjectViewType,
  InvitationStatus,
  OrganizationRole,
  Prisma
}
