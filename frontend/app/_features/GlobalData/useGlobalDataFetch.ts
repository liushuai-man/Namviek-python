import { orgGetBySlug } from '@/services/organization'
import { useGlobalDataStore } from '@/store/global'
import { getLocalCache, setLocalCache } from '@namviek/core/client'
import { useParams, useRouter } from 'next/navigation'
import { useEffect } from 'react'

const useOrgIdBySlug = () => {
  const { orgId, setOrgId, setOrgName } = useGlobalDataStore()
  const { orgName } = useParams()
  const { push } = useRouter()

  const fetchOrg = () => {
    orgGetBySlug(orgName).then(res => {
      const data = res.data?.data ?? res.data
      if (!data || !data.id || !data.slug) {
        push('/organization')
        return
      }
      setLocalCache('ORG_ID', data.id)
      setLocalCache('ORG_SLUG', data.slug)

      setOrgId(data.id)
      setOrgName(data.slug)
    }).catch(e => {
      push('/organization')
      console.error(e)
    })
  }

  useEffect(() => {
    if (!orgName) return

    const orgIdCache = getLocalCache('ORG_ID')
    const orgSlugCache = getLocalCache('ORG_SLUG')

    if (orgSlugCache === orgName && orgIdCache) {
      if (orgIdCache !== orgId) {
        setOrgId(orgIdCache)
        setOrgName(orgName)
        return
      }
    }

    if (orgSlugCache !== orgName) {
      fetchOrg()
    }

  }, [orgName, orgId])

}

export const useGlobalDataFetch = () => {
  useOrgIdBySlug()
}
