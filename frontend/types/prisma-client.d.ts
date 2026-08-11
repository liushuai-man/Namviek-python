// Type stubs replacing @prisma/client for the Python backend migration.
// The original NestJS+Prisma types are no longer generated; these interfaces
// keep the frontend compiling while the backend switch to FastAPI+MongoDB.

declare module '@prisma/client' {
  // ── Enums ────────────────────────────────────────────────────────

  export enum TaskPriority {
    NONE = 'NONE',
    LOW = 'LOW',
    MEDIUM = 'MEDIUM',
    HIGH = 'HIGH',
    URGENT = 'URGENT',
  }

  export enum StatusType {
    TODO = 'TODO',
    IN_PROGRESS = 'IN_PROGRESS',
    DONE = 'DONE',
  }

  export enum TaskType {
    TASK = 'TASK',
    SUBTASK = 'SUBTASK',
    BUG = 'BUG',
    STORY = 'STORY',
  }

  export enum MemberRole {
    ADMIN = 'ADMIN',
    MEMBER = 'MEMBER',
    GUEST = 'GUEST',
  }

  export enum UserStatus {
    ACTIVE = 'ACTIVE',
    INACTIVE = 'INACTIVE',
    PENDING = 'PENDING',
  }

  export enum OrgStorageType {
    LOCAL = 'LOCAL',
    S3 = 'S3',
    MINIO = 'MINIO',
  }

  export enum FieldType {
    TEXT = 'TEXT',
    NUMBER = 'NUMBER',
    DATE = 'DATE',
    PERSON = 'PERSON',
    SELECT = 'SELECT',
    CHECKBOX = 'CHECKBOX',
  }

  export enum FileType {
    IMAGE = 'IMAGE',
    DOCUMENT = 'DOCUMENT',
    VIDEO = 'VIDEO',
    AUDIO = 'AUDIO',
    OTHER = 'OTHER',
  }

  export enum FileOwnerType {
    TASK = 'TASK',
    PROJECT = 'PROJECT',
    USER = 'USER',
    ORGANIZATION = 'ORGANIZATION',
  }

  export enum ActivityType {
    CREATE = 'CREATE',
    UPDATE = 'UPDATE',
    DELETE = 'DELETE',
    COMMENT = 'COMMENT',
    ASSIGN = 'ASSIGN',
    STATUS_CHANGE = 'STATUS_CHANGE',
    PRIORITY_CHANGE = 'PRIORITY_CHANGE',
  }

  export enum ActivityObjectType {
    TASK = 'TASK',
    PROJECT = 'PROJECT',
    COMMENT = 'COMMENT',
    CHECKLIST = 'CHECKLIST',
  }

  export enum DashboardComponentType {
    CHART = 'CHART',
    TABLE = 'TABLE',
    STAT = 'STAT',
    CUSTOM = 'CUSTOM',
  }

  export enum ProjectViewType {
    LIST = 'LIST',
    BOARD = 'BOARD',
    CALENDAR = 'CALENDAR',
    GANTT = 'GANTT',
  }

  export enum InvitationStatus {
    PENDING = 'PENDING',
    ACCEPTED = 'ACCEPTED',
    REJECTED = 'REJECTED',
  }

  export enum OrganizationRole {
    OWNER = 'OWNER',
    ADMIN = 'ADMIN',
    MEMBER = 'MEMBER',
  }

  // ── Model interfaces ────────────────────────────────────────────

  export interface Organization {
    id: string
    name: string
    slug: string
    description: string
    desc?: string
    cover: string | null
    avatar?: string | null
    logo: string | null
    createdBy: string
    createdAt: string | Date
    updatedAt: string | Date | null
  }

  export interface User {
    id: string
    name: string
    email: string
    photo: string | null
    status: UserStatus
    createdAt: string | Date
    updatedAt: string | Date | null
  }

  export interface OrganizationMembers {
    id: string
    orgId: string
    uid: string
    role: OrganizationRole
    user?: User
    createdAt: string | Date
    updatedAt: string | Date | null
  }

  export interface Project {
    id: string
    orgId: string
    name: string
    description: string
    cover: string | null
    icon: string | null
    isArchived: boolean
    createdBy: string
    createdAt: string | Date
    updatedAt: string | Date | null
  }

  export interface Task {
    id: string
    projectId: string
    title: string
    desc: string
    statusId: string
    priority: TaskPriority
    type: TaskType
    order: number
    assigneeId: string | null
    dueDate: string | Date | null
    startDate: string | Date | null
    parentId: string | null
    createdBy: string
    createdAt: string | Date
    updatedAt: string | Date | null
    [key: string]: unknown
  }

  export interface TaskStatus {
    id: string
    projectId: string
    name: string
    color: string
    type: StatusType
    order: number
    createdAt: string | Date
    updatedAt: string | Date | null
  }

  export interface TaskPoint {
    id: string
    projectId: string
    name: string
    value: number
    createdAt: string | Date
    updatedAt: string | Date | null
  }

  export interface TaskChecklist {
    id: string
    taskId: string
    text: string
    checked: boolean
    order: number
    createdAt: string | Date
    updatedAt: string | Date | null
  }

  export interface TaskAutomation {
    id: string
    projectId: string
    name: string
    trigger: string
    action: string
    enabled: boolean
    config: Record<string, unknown>
    createdAt: string | Date
    updatedAt: string | Date | null
  }

  export interface Comment {
    id: string
    taskId: string
    content: string
    uid: string
    createdAt: string | Date
    updatedAt: string | Date | null
  }

  export interface Activity {
    id: string
    projectId: string
    taskId: string | null
    type: ActivityType
    objectType: ActivityObjectType
    content: string
    uid: string
    createdAt: string | Date
    updatedAt: string | Date | null
  }

  export interface ProjectView {
    id: string
    projectId: string
    name: string
    type: ProjectViewType
    config: Record<string, unknown>
    order: number
    createdAt: string | Date
    updatedAt: string | Date | null
  }

  export interface Field {
    id: string
    projectId: string
    name: string
    type: FieldType
    icon: string | null
    order: number
    visible: boolean
    createdAt: string | Date
    updatedAt: string | Date | null
  }

  export interface Vision {
    id: string
    projectId: string
    orgId: string
    title: string
    desc: string
    progress: number
    startDate: string | null
    endDate: string | null
    parentId: string | null
    createdBy: string
    createdAt: string | Date
    updatedAt: string | Date | null
  }

  export interface Favorites {
    id: string
    orgId: string
    uid: string
    projectId: string
    icon: string | null
    name: string | null
    type: string
    createdAt: string | Date
    updatedAt: string | Date | null
  }

  export interface DashboardComponent {
    id: string
    dboardId: string
    type: string
    title: string
    icon: string | null
    config: Record<string, unknown>
    x: number
    y: number
    width: number
    height: number
    createdAt: string | Date
    updatedAt: string | Date | null
  }

  export interface Application {
    id: string
    name: string
    icon: string | null
    url: string
    description: string
    orgId: string
    createdAt: string | Date
    updatedAt: string | Date | null
  }

  export interface FileStorage {
    id: string
    name: string
    type: FileType
    ownerType: FileOwnerType
    ownerId: string
    url: string
    size: number
    mimeType: string
    createdAt: string | Date
    updatedAt: string | Date | null
  }

  export interface ProjectSettingNotification {
    id: string
    projectId: string
    type: string
    enabled: boolean
    createdAt: string | Date
    updatedAt: string | Date | null
  }

  export interface Scheduler {
    id: string
    projectId: string
    name: string
    cron: string
    action: string
    enabled: boolean
    config: Record<string, unknown>
    createdAt: string | Date
    updatedAt: string | Date | null
  }

  // ── Prisma namespace ────────────────────────────────────────────

  export namespace Prisma {
    export type Json = unknown
    export type JsonObject = Record<string, unknown>
  }
}

declare module '.prisma/client' {
  export * from '@prisma/client'
}
