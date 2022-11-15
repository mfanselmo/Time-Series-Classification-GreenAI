<route lang="json">
{
    "meta": {
        "title": "Admin"
    }
}
</route>

<script setup lang="ts">

</script>

<template>
    <div class="grid grid-cols-1 lg:grid-cols-2">
        <div class="pr-8 my-auto">
            <process-data />
        </div>
        <div class="pl-8">
            <display-experiments />
        </div>
        <div class="col-span-2 mt-12">
            <completeness-curves />
        </div>
    </div>
</template>
