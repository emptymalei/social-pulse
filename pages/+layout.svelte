<script>
	import '@evidence-dev/tailwind/fonts.css';
	import '../app.css';
	import { EvidenceDefaultLayout } from '@evidence-dev/core-components';
	export let data;
</script>

<EvidenceDefaultLayout {data}
	neverShowQueries=true
	githubRepo="https://github.com/emptymalei/social-pulse"
	title="LM's Dashboard"
	fullWidth=true
>
	<slot slot="content" />
</EvidenceDefaultLayout>