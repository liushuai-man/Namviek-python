// Runtime shim replacing @prisma/client enums for the Python backend migration.
// Provides actual JavaScript values (not just TypeScript types).

export const TaskPriority = {
  NONE: 'NONE',
  LOW: 'LOW',
  MEDIUM: 'MEDIUM',
  NORMAL: 'NORMAL',
  HIGH: 'HIGH',
  URGENT: 'URGENT',
} as const

export const StatusType = {
  TODO: 'TODO',
  IN_PROGRESS: 'IN_PROGRESS',
  DONE: 'DONE',
} as const

export const TaskType = {
  TASK: 'TASK',
  SUBTASK: 'SUBTASK',
  BUG: 'BUG',
  STORY: 'STORY',
} as const

export const MemberRole = {
  ADMIN: 'ADMIN',
  MEMBER: 'MEMBER',
  GUEST: 'GUEST',
} as const

export const UserStatus = {
  ACTIVE: 'ACTIVE',
  INACTIVE: 'INACTIVE',
  PENDING: 'PENDING',
} as const

export const OrgStorageType = {
  LOCAL: 'LOCAL',
  S3: 'S3',
  MINIO: 'MINIO',
} as const

export const FieldType = {
  TEXT: 'TEXT',
  NUMBER: 'NUMBER',
  DATE: 'DATE',
  PERSON: 'PERSON',
  SELECT: 'SELECT',
  CHECKBOX: 'CHECKBOX',
} as const

export const FileType = {
  IMAGE: 'IMAGE',
  DOCUMENT: 'DOCUMENT',
  VIDEO: 'VIDEO',
  AUDIO: 'AUDIO',
  OTHER: 'OTHER',
} as const

export const FileOwnerType = {
  TASK: 'TASK',
  PROJECT: 'PROJECT',
  USER: 'USER',
  ORGANIZATION: 'ORGANIZATION',
} as const

export const ActivityType = {
  CREATE: 'CREATE',
  UPDATE: 'UPDATE',
  DELETE: 'DELETE',
  COMMENT: 'COMMENT',
  ASSIGN: 'ASSIGN',
  STATUS_CHANGE: 'STATUS_CHANGE',
  PRIORITY_CHANGE: 'PRIORITY_CHANGE',
} as const

export const ActivityObjectType = {
  TASK: 'TASK',
  PROJECT: 'PROJECT',
  COMMENT: 'COMMENT',
  CHECKLIST: 'CHECKLIST',
} as const

export const DashboardComponentType = {
  CHART: 'CHART',
  TABLE: 'TABLE',
  STAT: 'STAT',
  CUSTOM: 'CUSTOM',
} as const

export const ProjectViewType = {
  LIST: 'LIST',
  BOARD: 'BOARD',
  CALENDAR: 'CALENDAR',
  GANTT: 'GANTT',
} as const

export const InvitationStatus = {
  PENDING: 'PENDING',
  ACCEPTED: 'ACCEPTED',
  REJECTED: 'REJECTED',
} as const

export const OrganizationRole = {
  OWNER: 'OWNER',
  ADMIN: 'ADMIN',
  MEMBER: 'MEMBER',
} as const

// Also export as Prisma namespace-compatible object
export const Prisma = {
  Json: {} as unknown,
}
