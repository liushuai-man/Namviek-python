// Runtime shim replacing @prisma/client enums for the Python backend migration.
// Provides actual JavaScript values (not just TypeScript types).
// This file is loaded at runtime via webpack alias configured in next.config.js.

const TaskPriority = Object.freeze({
  NONE: 'NONE',
  LOW: 'LOW',
  MEDIUM: 'MEDIUM',
  NORMAL: 'NORMAL',
  HIGH: 'HIGH',
  URGENT: 'URGENT',
})

const StatusType = Object.freeze({
  TODO: 'TODO',
  IN_PROGRESS: 'IN_PROGRESS',
  DONE: 'DONE',
})

const TaskType = Object.freeze({
  TASK: 'TASK',
  SUBTASK: 'SUBTASK',
  BUG: 'BUG',
  STORY: 'STORY',
})

const MemberRole = Object.freeze({
  ADMIN: 'ADMIN',
  MEMBER: 'MEMBER',
  GUEST: 'GUEST',
})

const UserStatus = Object.freeze({
  ACTIVE: 'ACTIVE',
  INACTIVE: 'INACTIVE',
  PENDING: 'PENDING',
})

const OrgStorageType = Object.freeze({
  LOCAL: 'LOCAL',
  S3: 'S3',
  MINIO: 'MINIO',
})

const FieldType = Object.freeze({
  TEXT: 'TEXT',
  NUMBER: 'NUMBER',
  DATE: 'DATE',
  PERSON: 'PERSON',
  SELECT: 'SELECT',
  CHECKBOX: 'CHECKBOX',
})

const FileType = Object.freeze({
  IMAGE: 'IMAGE',
  DOCUMENT: 'DOCUMENT',
  VIDEO: 'VIDEO',
  AUDIO: 'AUDIO',
  OTHER: 'OTHER',
})

const FileOwnerType = Object.freeze({
  TASK: 'TASK',
  PROJECT: 'PROJECT',
  USER: 'USER',
  ORGANIZATION: 'ORGANIZATION',
})

const ActivityType = Object.freeze({
  CREATE: 'CREATE',
  UPDATE: 'UPDATE',
  DELETE: 'DELETE',
  COMMENT: 'COMMENT',
  ASSIGN: 'ASSIGN',
  STATUS_CHANGE: 'STATUS_CHANGE',
  PRIORITY_CHANGE: 'PRIORITY_CHANGE',
})

const ActivityObjectType = Object.freeze({
  TASK: 'TASK',
  PROJECT: 'PROJECT',
  COMMENT: 'COMMENT',
  CHECKLIST: 'CHECKLIST',
})

const DashboardComponentType = Object.freeze({
  CHART: 'CHART',
  TABLE: 'TABLE',
  STAT: 'STAT',
  CUSTOM: 'CUSTOM',
})

const ProjectViewType = Object.freeze({
  LIST: 'LIST',
  BOARD: 'BOARD',
  CALENDAR: 'CALENDAR',
  GANTT: 'GANTT',
})

const InvitationStatus = Object.freeze({
  PENDING: 'PENDING',
  ACCEPTED: 'ACCEPTED',
  REJECTED: 'REJECTED',
})

const OrganizationRole = Object.freeze({
  OWNER: 'OWNER',
  ADMIN: 'ADMIN',
  MEMBER: 'MEMBER',
})

const Prisma = Object.freeze({
  Json: {},
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
  Prisma,
}
