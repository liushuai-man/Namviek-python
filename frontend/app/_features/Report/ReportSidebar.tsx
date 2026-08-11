import ReportSavedListContainer from "../ReportSavedList"
import ReportFilterMember from "./ReportFilterMember"
import ReportFilterProject from "./ReportFilterProject"

export default function ReportSidebar() {
  return <section className='report-sidebar'>
    <ReportSavedListContainer />
    <ReportFilterProject />
    <ReportFilterMember />
  </section>
}
