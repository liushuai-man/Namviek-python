import { Organization } from '@prisma/client';
import { httpGet, httpPost } from './_req';

export const orgCreate = (data: Partial<Organization>) => {
  return httpPost('/api/org', data).then(res => {
    const { data: resData } = res.data
    const organization = resData as Organization
    return Promise.resolve(organization)
  });
};

export const orgGet = () => {
  return httpGet('/api/org');
};
